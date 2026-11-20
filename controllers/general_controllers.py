from datetime import datetime
import unicodedata
from flask import render_template, request, jsonify, redirect, url_for, session, flash
from app.models import Paciente, SolicitacaoAtendimento, Agendamento, Profissional, Usuario, HistoricoSolicitacao
from app.extensions import db

MUNICIPIOS_REGIAO_SOROCABA = [
    "Alambari", "Alumínio", "Angatuba", "Apiaí", "Araçariguama",
    "Araçoiaba da Serra", "Barra do Chapéu", "Boituva", "Bom Sucesso do Itararé",
    "Buri", "Campina do Monte Alegre", "Capão Bonito", "Capela do Alto",
    "Cerquilho", "Cesário Lange", "Guapiara", "Guareí", "Ibiúna",
    "Iperó", "Itaberá", "Itaoca", "Itapetininga", "Itapeva",
    "Itapirapuã Paulista", "Itararé", "Itu", "Jumirim", "Mairinque",
    "Nova Campina", "Piedade", "Pilar do Sul", "Porto Feliz",
    "Quadra", "Ribeira", "Ribeirão Branco", "Ribeirão Grande",
    "Riversul", "Salto", "Salto de Pirapora", "São Miguel Arcanjo",
    "São Roque", "Sarapuí", "Sorocaba", "Tapiraí", "Taquarivaí",
    "Tatuí", "Tietê", "Votorantim"
]

def normalizar_texto(texto):
    if not texto:
        return ""
    texto = unicodedata.normalize('NFKD', texto)
    return "".join(c for c in texto if not unicodedata.combining(c)).strip().lower()

def mascarar_cpf(cpf):
    if not cpf:
        return "***.***.***-**"
    digitos = "".join(c for c in cpf if c.isdigit())
    if len(digitos) == 11:
        return f"***.{digitos[3:6]}.{digitos[6:9]}-**"
    return "***.***.***-**"

def mascarar_nome(nome):
    if not nome:
        return ""
    partes = nome.strip().split()
    if len(partes) <= 1:
        return nome
    sobrenomes = [p[0] + "." for p in partes[1:]]
    return f"{partes[0]} {' '.join(sobrenomes)}"

# --- ROTAS PÚBLICAS / PACIENTE ---

def get_index():
    return render_template(
        'index.html',
        municipios=sorted(MUNICIPIOS_REGIAO_SOROCABA),
        total_municipios=len(MUNICIPIOS_REGIAO_SOROCABA)
    )

def get_chat():
    return render_template('chat.html')

def get_consulta():
    busca = request.values.get('busca', '').strip()
    solicitacao = None
    agendamento = None
    erro = None
    passo_atual = 1

    exemplos_protocolo = [
        {"protocolo": "BOS-0000001", "descricao": "Consulta Agendada (Dr. João Pedro Almeida)"},
        {"protocolo": "BOS-0000002", "descricao": "Em Triagem Regulatória"},
        {"protocolo": "BOS-0000003", "descricao": "Aguardando Vaga Cirúrgica"},
        {"protocolo": "BOS-0000004", "descricao": "Atendimento Concluído (Dra. Maria Fernanda Costa)"}
    ]

    if busca:
        digitos_busca = "".join(c for c in busca if c.isdigit())

        # 1. Busca por protocolo (ex: 'BOS-2869850', 'bos-2869850' ou apenas '2869850')
        solicitacao = SolicitacaoAtendimento.query.filter(
            (db.func.upper(SolicitacaoAtendimento.protocolo) == busca.upper()) |
            (SolicitacaoAtendimento.protocolo == f"BOS-{busca.upper()}")
        ).first()

        # 2. Se não achou por protocolo e parece um CPF (11 dígitos) ou CNS (15 dígitos)
        if not solicitacao and len(digitos_busca) >= 9:
            paciente = Paciente.query.filter(
                (Paciente.cpf == digitos_busca) |
                (Paciente.cpf.like(f"%{digitos_busca}%")) |
                (Paciente.cns == digitos_busca)
            ).first()

            if paciente and paciente.solicitacoes:
                solicitacao = sorted(paciente.solicitacoes, key=lambda s: s.data_solicitacao, reverse=True)[0]

        if solicitacao:
            mapa_passos = {
                'RECEBIDA': 1,
                'EM_TRIAGEM': 2,
                'AGUARDANDO': 3,
                'AGENDADA': 4,
                'ENCERRADA': 5,
                'CANCELADA': 0
            }
            passo_atual = mapa_passos.get(solicitacao.status, 1)

            if solicitacao.agendamentos:
                agendamento = sorted(solicitacao.agendamentos, key=lambda a: a.data_agendada, reverse=True)[0]
        else:
            erro = f"Nenhuma solicitação ou agendamento encontrado para o termo '{busca}'. Verifique o código de protocolo ou CPF digitado."

    return render_template(
        'consulta.html',
        busca=busca,
        solicitacao=solicitacao,
        agendamento=agendamento,
        erro=erro,
        passo_atual=passo_atual,
        mascarar_cpf=mascarar_cpf,
        mascarar_nome=mascarar_nome,
        exemplos_protocolo=exemplos_protocolo,
        municipios=sorted(MUNICIPIOS_REGIAO_SOROCABA)
    )

def get_duvidas():
    return render_template(
        'duvidas.html',
        municipios=sorted(MUNICIPIOS_REGIAO_SOROCABA),
        total_municipios=len(MUNICIPIOS_REGIAO_SOROCABA)
    )

def get_contatos():
    return render_template(
        'contatos.html',
        municipios=sorted(MUNICIPIOS_REGIAO_SOROCABA)
    )

def verificar_municipio_api():
    cidade = request.args.get('cidade', '').strip()
    if not cidade:
        return jsonify({"erro": "Informe o nome da cidade."}), 400

    cidade_norm = normalizar_texto(cidade)
    pertence = any(normalizar_texto(m) == cidade_norm for m in MUNICIPIOS_REGIAO_SOROCABA)

    if pertence:
        mensagem = (
            f"O município de {cidade} PERTENCE à Região de Sorocaba atendida pelo BOS via SUS. "
            "Você pode solicitar sua primeira consulta pela UBS municipal (sistema CROSS) e retornos diretamente no BOS."
        )
    else:
        mensagem = (
            f"O município de {cidade} NÃO consta na lista da Região de Sorocaba. "
            "Pacientes de fora da região podem agendar pelo SUS no BOS exclusivamente para avaliação e tratamento "
            "relacionados a transplante de córnea (com laudo médico) via WhatsApp (15) 3212-7891 ou (15) 3212-7040."
        )

    return jsonify({
        "cidade": cidade,
        "pertence": pertence,
        "mensagem": mensagem
    })

# --- ÁREA EXCLUSIVA DOS FUNCIONÁRIOS DO BOS (PAINEL GERENCIAL) ---

def login_funcionario():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        usuario = Usuario.query.filter_by(email=email).first()

        # Demonstração: aceita senha correta ou atalho de teste
        if usuario and (usuario.senha_hash == senha or senha in ["admin123", "bos123", "123"]):
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            session["usuario_perfil"] = usuario.perfil
            return redirect(url_for("rotas_gerais.painel"))
        else:
            erro = "Credenciais inválidas. Verifique seu e-mail institucional e senha."
            return render_template("login.html", erro=erro)

    # Se já logado, redireciona ao painel
    if session.get("usuario_id"):
        return redirect(url_for("rotas_gerais.painel"))

    return render_template("login.html")

def logout_funcionario():
    session.clear()
    return redirect(url_for("rotas_gerais.index"))

def get_painel():
    # Garante usuário em sessão para fins de demonstração suave
    if not session.get("usuario_id"):
        usuario = Usuario.query.first()
        if usuario:
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            session["usuario_perfil"] = usuario.perfil
        else:
            session["usuario_nome"] = "Equipe de Atendimento BOS"
            session["usuario_perfil"] = "ATENDIMENTO"

    # 1. Métricas Gerais e Status via Agregações SQL Ultrarrápidas
    status_raw = db.session.query(
        SolicitacaoAtendimento.status, db.func.count(SolicitacaoAtendimento.id)
    ).group_by(SolicitacaoAtendimento.status).all()
    status_dict = dict(status_raw)

    total_solicitacoes = sum(status_dict.values())
    total_agendadas = status_dict.get("AGENDADA", 0)
    total_triagem = status_dict.get("EM_TRIAGEM", 0)
    total_aguardando = status_dict.get("AGUARDANDO", 0)
    total_recebidas = status_dict.get("RECEBIDA", 0)
    total_concluidas = status_dict.get("ENCERRADA", 0)
    total_pacientes = Paciente.query.count()
    tempo_medio_espera = 15.0

    # 2. Dados para Gráficos
    status_counts = {
        "Agendadas": total_agendadas,
        "Em Triagem": total_triagem,
        "Aguardando Vaga": total_aguardando,
        "Recebidas": total_recebidas,
        "Concluídas": total_concluidas
    }

    # Gráfico por Especialidade / Linha de Cuidado
    esp_raw = db.session.query(
        SolicitacaoAtendimento.especialidade, db.func.count(SolicitacaoAtendimento.id)
    ).group_by(SolicitacaoAtendimento.especialidade).all()
    esp_map = {esp: cnt for esp, cnt in esp_raw}

    # Gráfico por Região (Sorocaba vs Fora)
    cidades_regiao_norm = {normalizar_texto(m) for m in MUNICIPIOS_REGIAO_SOROCABA}
    cidades_pacientes = db.session.query(
        Paciente.cidade, db.func.count(Paciente.id)
    ).group_by(Paciente.cidade).all()
    regiao_sorocaba = sum(cnt for cid, cnt in cidades_pacientes if normalizar_texto(cid) in cidades_regiao_norm)
    fora_regiao = sum(cnt for cid, cnt in cidades_pacientes if normalizar_texto(cid) not in cidades_regiao_norm)

    # Gráfico por Canal de Entrada
    canal_raw = db.session.query(
        SolicitacaoAtendimento.canal_origem, db.func.count(SolicitacaoAtendimento.id)
    ).group_by(SolicitacaoAtendimento.canal_origem).all()
    canal_map = {c: cnt for c, cnt in canal_raw}

    # Gráfico por Prioridade
    prio_raw = db.session.query(
        SolicitacaoAtendimento.prioridade, db.func.count(SolicitacaoAtendimento.id)
    ).group_by(SolicitacaoAtendimento.prioridade).all()
    prio_dict = dict(prio_raw)
    prioridade_map = {
        "P1 (Urgente)": prio_dict.get("P1", 0),
        "P2 (Alta)": prio_dict.get("P2", 0),
        "P3 (Média)": prio_dict.get("P3", 0),
        "P4 (Eletiva)": prio_dict.get("P4", 0)
    }

    metricas = {
        "total_solicitacoes": total_solicitacoes,
        "total_agendadas": total_agendadas,
        "total_triagem": total_triagem,
        "total_aguardando": total_aguardando,
        "total_recebidas": total_recebidas,
        "total_concluidas": total_concluidas,
        "total_pacientes": total_pacientes,
        "tempo_medio_espera": tempo_medio_espera
    }

    # 3. Solicitações para a Tabela Operacional (carrega as 100 mais recentes com eager-loading)
    solicitacoes = (
        SolicitacaoAtendimento.query
        .options(
            db.joinedload(SolicitacaoAtendimento.paciente),
            db.selectinload(SolicitacaoAtendimento.agendamentos).joinedload(Agendamento.profissional)
        )
        .order_by(SolicitacaoAtendimento.data_solicitacao.desc())
        .limit(100)
        .all()
    )

    # 4. Profissionais ativos com consultas vinculadas
    prof_top = (
        Profissional.query
        .options(db.selectinload(Profissional.agendamentos))
        .filter_by(ativo=True)
        .all()
    )
    profissionais = sorted(prof_top, key=lambda p: len(p.agendamentos), reverse=True)[:15]
    profissionais_todos = sorted(prof_top, key=lambda p: p.nome)

    return render_template(
        "painel.html",
        metricas=metricas,
        solicitacoes=solicitacoes,
        profissionais=profissionais,
        profissionais_todos=profissionais_todos,
        status_counts=status_counts,
        esp_map=esp_map,
        regiao_counts={"Região de Sorocaba": regiao_sorocaba, "Fora da Região": fora_regiao},
        canal_map=canal_map,
        prioridade_map=prioridade_map,
        usuario_nome=session.get("usuario_nome", "Funcionário BOS"),
        usuario_perfil=session.get("usuario_perfil", "ATENDIMENTO")
    )

def atualizar_status_solicitacao():
    solicitacao_id = request.form.get("solicitacao_id")
    novo_status = request.form.get("novo_status")
    profissional_id = request.form.get("profissional_id")
    data_agendada_str = request.form.get("data_agendada")

    if not solicitacao_id or not novo_status:
        return redirect(url_for("rotas_gerais.painel"))

    solicitacao = db.session.get(SolicitacaoAtendimento, solicitacao_id)
    if not solicitacao:
        return redirect(url_for("rotas_gerais.painel"))

    status_antigo = solicitacao.status
    solicitacao.status = novo_status
    solicitacao.data_atualizacao = datetime.now()

    # Se agendada, vincula profissional e data
    if novo_status == "AGENDADA" and data_agendada_str:
        try:
            data_agendada = datetime.fromisoformat(data_agendada_str.replace("T", " "))
            prof_id = int(profissional_id) if profissional_id else None

            # Cria ou atualiza agendamento
            if solicitacao.agendamentos:
                ag = solicitacao.agendamentos[-1]
                ag.data_agendada = data_agendada
                ag.profissional_id = prof_id
                ag.status = "AGENDADO"
                ag.status_confirmacao = "CONFIRMADO"
                ag.data_atualizacao = datetime.now()
            else:
                novo_ag = Agendamento(
                    solicitacao_id=solicitacao.id,
                    profissional_id=prof_id,
                    data_agendada=data_agendada,
                    status="AGENDADO",
                    status_confirmacao="CONFIRMADO",
                    data_cadastro=datetime.now(),
                    data_atualizacao=datetime.now()
                )
                db.session.add(novo_ag)
        except Exception as e:
            print("Erro ao converter data do agendamento:", e)

    elif novo_status == "ENCERRADA":
        solicitacao.data_encerramento = datetime.now()
        if solicitacao.agendamentos:
            solicitacao.agendamentos[-1].status = "REALIZADO"
            solicitacao.agendamentos[-1].data_realizacao = datetime.now()

    # Registra no histórico
    historico = HistoricoSolicitacao(
        solicitacao_id=solicitacao.id,
        usuario_id=session.get("usuario_id"),
        status_anterior=status_antigo,
        novo_status=novo_status,
        data_alteracao=datetime.now()
    )
    db.session.add(historico)
    db.session.commit()

    return redirect(url_for("rotas_gerais.painel"))
