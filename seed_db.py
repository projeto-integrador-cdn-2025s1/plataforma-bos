"""
Script de povoamento (seed) para o banco de dados do Banco de Olhos de Sorocaba (BOS).
Versão com DADOS FICTÍCIOS - Não utiliza dados reais de pacientes.
Gera usuários gerenciais, profissionais, pacientes fictícios com endereços e cidades da região,
solicitações de atendimento e agendamentos vinculados.
"""

import random
import re
import sqlite3
import unicodedata
from datetime import datetime, timedelta, date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "instance" / "bos.db"

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

# Nomes fictícios brasileiros
NOMES_PRIMEIROS = [
    "Ana", "Maria", "José", "João", "Antônio", "Francisco", "Carlos", "Paulo", "Pedro", "Lucas",
    "Mariana", "Juliana", "Amanda", "Beatriz", "Camila", "Fernanda", "Gabriela", "Isabela", "Larissa", "Letícia",
    "Rafael", "Gabriel", "Felipe", "Gustavo", "Henrique", "Leonardo", "Matheus", "Vinícius", "Bruno", "Diego",
    "Patrícia", "Sandra", "Roberta", "Tatiana", "Vanessa", "Adriana", "Mônica", "Cláudia", "Luciana", "Renata",
    "Ricardo", "Rodrigo", "Marcelo", "André", "Fábio", "Alexandre", "Eduardo", "Thiago", "Leandro", "Márcio"
]

SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Almeida", "Pereira", "Lima", "Gomes",
    "Costa", "Ribeiro", "Martins", "Carvalho", "Alves", "Lopes", "Soares", "Fernandes", "Vieira", "Barbosa",
    "Rocha", "Dias", "Monteiro", "Mendes", "Nascimento", "Cavalcanti", "Araújo", "Correia", "Cardoso", "Cruz",
    "Melo", "Pinto", "Castro", "Campos", "Teixeira", "Freitas", "Machado", "Moraes", "Nunes", "Moreira"
]

NOMES_MAE = [
    "Maria da Silva", "Ana Santos", "Joséfa Oliveira", "Francisca Souza", "Antônia Rodrigues",
    "Francisca Ferreira", "Maria Almeida", "Josefa Pereira", "Ana Lima", "Maria Gomes"
]

RUAS = [
    "Rua das Flores", "Av. Presidente Vargas", "Rua 15 de Novembro", "Av. São Paulo",
    "Rua do Comércio", "Av. Dom Aguirre", "Rua da Penha", "Av. Dr. Armando Pannunzio",
    "Rua Santa Cruz", "Av. Itavuvu", "Rua XV de Novembro", "Av. Eng. Carlos Reinaldo Mendes",
    "Rua Henrique Gregori", "Av. Afonso Vergueiro", "Rua Cel. Nogueira Padilha", "Av. Brasil",
    "Rua Sete de Setembro", "Av. Antônio Carlos Comitre", "Rua Artur Caldas", "Av. Maria Cinto de Biaggi"
]

BAIRROS = [
    "Centro", "Vila Haro", "Jardim Santa Rosália", "Vila Helena", "Jardim América",
    "Vila Progresso", "Jardim São Paulo", "Vila Assis", "Jardim Faculdade", "Vila Guiomar",
    "Além Ponte", "Jardim Vergueiro", "Vila Santana", "Jardim Monterrey", "Vila Barão",
    "Jardim Europa", "Vila Hortência", "Jardim Ipiranga", "Vila Trujillo", "Jardim São Carlos"
]

ESPECIALIDADES = [
    "Catarata e Cirurgia Refrativa",
    "Retina e Vítreo",
    "Glaucoma",
    "Córnea e Doenças Externas",
    "Oftalmologia Geral",
    "Pós-Operatório / Retorno",
    "Plástica Ocular",
    "Estrabismo"
]

PROCEDIMENTOS = [
    "Facoemulsificação com Implante de LIO",
    "Facectomia Extracapsular",
    "Vitrectomia Posterior",
    "Trabeculectomia",
    "Transplante de Córnea (Penetrante)",
    "Transplante de Córnea (Lamelar)",
    "Injeção Intravítrea de Anti-VEGF",
    "Laser de Retina (Fotocoagulação)",
    "Cirurgia de Pterígio",
    "Blefaroplastia",
    "Correção de Ptose Palpebral",
    "Cirurgia de Estrabismo",
    "Implante de Anel Intraestromal",
    "Crosslinking de Córnea",
    "Capsulotomia a Laser (YAG)"
]

CIDS = [
    "H25.9", "H26.9", "H40.9", "H35.3", "H33.0", "H18.9", "H11.0", "H02.4",
    "H52.5", "H54.7", "Z54.0", "H16.0", "H18.6", "H35.0", "H43.0"
]

TIPOS_ATENDIMENTO = [
    "Primeira Consulta",
    "Retorno Ambulatorial",
    "Procedimento Cirúrgico",
    "Avaliação Especializada"
]

CANAIS = ["BALCAO", "TELEFONE", "WHATSAPP", "EMAIL", "OUTRO"]
PRIORIDADES = ["P1", "P2", "P3", "P4"]
STATUSES = ["RECEBIDA", "EM_TRIAGEM", "AGUARDANDO", "AGENDADA", "ENCERRADA", "CANCELADA"]

HORARIOS = [
    (8, 0), (8, 30), (9, 0), (9, 30), (10, 0), (10, 30), (11, 0), (11, 30),
    (13, 30), (14, 0), (14, 30), (15, 0), (15, 30), (16, 0), (16, 30), (17, 0)
]

def norm(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text)
    return "".join(c for c in text if not unicodedata.combining(c)).strip().upper()

MUNICIPIOS_DICT = {norm(m): m for m in MUNICIPIOS_REGIAO_SOROCABA}

def gerar_cpf():
    """Gera CPF válido fictício"""
    base = [random.randint(0, 9) for _ in range(9)]
    for peso in [10, 11]:
        soma = sum(base[i] * (peso - i) for i in range(peso - 1))
        digito = 11 - (soma % 11)
        if digito >= 10:
            digito = 0
        base.append(digito)
    return "".join(map(str, base))

def gerar_cns():
    """Gera CNS fictício (15 dígitos)"""
    return "".join(str(random.randint(0, 9)) for _ in range(15))

def gerar_telefone():
    """Gera telefone fictício"""
    ddd = random.choice(["11", "15", "16", "17", "18", "19"])
    numero = f"{random.randint(2000, 9999)}-{random.randint(1000, 9999)}"
    return f"({ddd}) {numero}"

def gerar_cep():
    """Gera CEP fictício da região de Sorocaba"""
    return f"18{random.randint(000, 999):03d}-{random.randint(100, 999):03d}"

def gerar_email(nome):
    """Gera email fictício"""
    base = nome.lower().replace(" ", ".")
    base = "".join(c for c in base if c.isalnum() or c == ".")
    dominios = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com.br", "bol.com.br"]
    return f"{base}{random.randint(1, 999)}@{random.choice(dominios)}"

def gerar_nome_completo():
    """Gera nome completo fictício"""
    primeiro = random.choice(NOMES_PRIMEIROS)
    sobrenome1 = random.choice(SOBRENOMES)
    sobrenome2 = random.choice(SOBRENOMES)
    return f"{primeiro} {sobrenome1} {sobrenome2}"

def gerar_data_nascimento():
    """Gera data de nascimento entre 1930 e 2010"""
    ano = random.randint(1930, 2010)
    mes = random.randint(1, 12)
    dia = random.randint(1, 28)
    return date(ano, mes, dia)

def gerar_endereco():
    """Gera endereço fictício"""
    rua = random.choice(RUAS)
    numero = str(random.randint(1, 9999))
    bairro = random.choice(BAIRROS)
    cidade = random.choice(MUNICIPIOS_REGIAO_SOROCABA)
    estado = "SP"
    cep = gerar_cep()
    return rua, numero, bairro, cidade, estado, cep

def popular_banco():
    print("Iniciando povoamento com DADOS FICTÍCIOS...")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # Cria tabelas se não existirem
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(150) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        senha_hash VARCHAR(255) NOT NULL,
        perfil VARCHAR(20) NOT NULL DEFAULT 'ATENDIMENTO',
        ativo BOOLEAN NOT NULL DEFAULT 1,
        data_cadastro DATETIME NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY,
        nome_completo VARCHAR(150) NOT NULL,
        data_nascimento DATE,
        nome_mae VARCHAR(150),
        cpf VARCHAR(11) UNIQUE,
        cns VARCHAR(15) UNIQUE,
        telefone VARCHAR(20) NOT NULL,
        email VARCHAR(150),
        cep VARCHAR(8),
        rua VARCHAR(150),
        numero VARCHAR(15),
        complemento VARCHAR(100),
        bairro VARCHAR(100),
        cidade VARCHAR(100),
        estado VARCHAR(2),
        data_cadastro DATETIME NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS profissionais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(150) NOT NULL,
        especialidade VARCHAR(120) NOT NULL,
        ativo BOOLEAN NOT NULL DEFAULT 1
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS solicitacoes_atendimento (
        id INTEGER PRIMARY KEY,
        protocolo VARCHAR(20) UNIQUE NOT NULL,
        paciente_id INTEGER NOT NULL REFERENCES pacientes(id),
        prioridade VARCHAR(2) NOT NULL,
        possui_pedido_medico BOOLEAN NOT NULL DEFAULT 0,
        cid VARCHAR(10),
        motivo_clinico TEXT,
        tipo_atendimento VARCHAR(30) NOT NULL,
        especialidade VARCHAR(120) NOT NULL,
        procedimento VARCHAR(150),
        canal_origem VARCHAR(20) NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'RECEBIDA',
        data_solicitacao DATETIME NOT NULL,
        data_atualizacao DATETIME NOT NULL,
        data_encerramento DATETIME
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        solicitacao_id INTEGER NOT NULL REFERENCES solicitacoes_atendimento(id),
        profissional_id INTEGER REFERENCES profissionais(id),
        data_agendada DATETIME NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'AGENDADO',
        status_confirmacao VARCHAR(20) NOT NULL DEFAULT 'PENDENTE',
        data_realizacao DATETIME,
        data_cadastro DATETIME NOT NULL,
        data_atualizacao DATETIME NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS historico_solicitacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        solicitacao_id INTEGER NOT NULL REFERENCES solicitacoes_atendimento(id),
        usuario_id INTEGER,
        status_anterior VARCHAR(20),
        novo_status VARCHAR(20) NOT NULL,
        data_alteracao DATETIME NOT NULL
    )
    """)

    # Limpa dados existentes
    cur.execute("DELETE FROM historico_solicitacoes")
    cur.execute("DELETE FROM agendamentos")
    cur.execute("DELETE FROM solicitacoes_atendimento")
    cur.execute("DELETE FROM profissionais")
    cur.execute("DELETE FROM pacientes")
    cur.execute("DELETE FROM usuarios")

    agora = datetime.now()

    # 1. Usuários para acesso ao painel gerencial
    usuarios = [
        (1, "Coordenação de Atendimento SUS", "atendimento@bos.org.br", "bos123", "ATENDIMENTO", 1, agora.strftime("%Y-%m-%d %H:%M:%S")),
        (2, "Gestor Geral BOS", "admin@bos.org.br", "admin123", "ADMIN", 1, agora.strftime("%Y-%m-%d %H:%M:%S"))
    ]
    cur.executemany("INSERT INTO usuarios (id, nome, email, senha_hash, perfil, ativo, data_cadastro) VALUES (?, ?, ?, ?, ?, ?, ?)", usuarios)
    print("[OK] Usuarios de acesso cadastrados.")

    # 2. Profissionais médicos fictícios
    medicos_nomes = [
        "Dr. João Pedro Almeida",
        "Dra. Maria Fernanda Costa",
        "Dr. Carlos Eduardo Silva",
        "Dra. Ana Paula Santos",
        "Dr. Roberto Carlos Lima",
        "Dra. Juliana Mendes Oliveira",
        "Dr. Felipe Augusto Rocha",
        "Dra. Gabriela Ferreira Souza",
        "Dr. Marcos Vinícius Pereira",
        "Dra. Patricia Regina Martins"
    ]

    profissionais_rows = []
    for idx, med_nome in enumerate(medicos_nomes, start=1):
        especialidade = random.choice(ESPECIALIDADES)
        profissionais_rows.append((idx, med_nome, especialidade, 1))

    cur.executemany("INSERT INTO profissionais (id, nome, especialidade, ativo) VALUES (?, ?, ?, ?)", profissionais_rows)
    print(f"[OK] {len(profissionais_rows)} Profissionais médicos fictícios cadastrados.")

    # 3. Pacientes fictícios
    NUM_PACIENTES = 5000
    pacientes_rows = []
    cpfs_inseridos = set()
    cnss_inseridos = set()

    for pid in range(1, NUM_PACIENTES + 1):
        nome = gerar_nome_completo()
        dt_nasc = gerar_data_nascimento()
        dt_nasc_str = dt_nasc.strftime("%Y-%m-%d")

        nome_mae = random.choice(NOMES_MAE)

        # CPF único
        cpf = None
        tentativas = 0
        while cpf is None and tentativas < 10:
            cpf_gerado = gerar_cpf()
            if cpf_gerado not in cpfs_inseridos:
                cpf = cpf_gerado
                cpfs_inseridos.add(cpf)
            tentativas += 1

        # CNS único
        cns = None
        tentativas = 0
        while cns is None and tentativas < 10:
            cns_gerado = gerar_cns()
            if cns_gerado not in cnss_inseridos:
                cns = cns_gerado
                cnss_inseridos.add(cns)
            tentativas += 1

        telefone = gerar_telefone()
        email = gerar_email(nome) if random.random() > 0.3 else None

        rua, numero, bairro, cidade, estado, cep = gerar_endereco()

        # Data de cadastro aleatória nos últimos 2 anos
        dias_atras = random.randint(0, 730)
        dt_cad = (datetime.now() - timedelta(days=dias_atras)).strftime("%Y-%m-%d %H:%M:%S")

        pacientes_rows.append((
            pid, nome, dt_nasc_str, nome_mae, cpf, cns, telefone, email,
            cep.replace("-", ""), rua, numero, None, bairro, cidade, estado, dt_cad
        ))

    cur.executemany("""
    INSERT INTO pacientes (
        id, nome_completo, data_nascimento, nome_mae, cpf, cns, telefone, email,
        cep, rua, numero, complemento, bairro, cidade, estado, data_cadastro
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, pacientes_rows)
    print(f"[OK] {len(pacientes_rows)} Pacientes fictícios cadastrados.")

    # 4. Solicitações de Atendimento e Agendamentos
    NUM_SOLICITACOES = 15000
    solicitacoes_rows = []
    agendamentos_rows = []
    historico_rows = []

    agendamento_id_seq = 1
    historico_id_seq = 1

    # Criar mapa de pacientes por ID
    paciente_ids = list(range(1, NUM_PACIENTES + 1))

    for aid in range(1, NUM_SOLICITACOES + 1):
        pid = random.choice(paciente_ids)
        protocolo = f"BOS-{aid:07d}"

        # Data de atendimento base (últimos 18 meses)
        dias_atras_atend = random.randint(0, 540)
        dt_atend = datetime.now() - timedelta(days=dias_atras_atend)

        h_idx = aid % len(HORARIOS)
        hora, minuto = HORARIOS[h_idx]
        dt_agendada = dt_atend.replace(hour=hora, minute=minuto)

        # Prioridade
        prioridade = random.choices(PRIORIDADES, weights=[5, 20, 40, 35])[0]

        possui_pedido_medico = random.choice([0, 1])

        cid = random.choice(CIDS) if random.random() > 0.2 else None
        procedimento = random.choice(PROCEDIMENTOS) if random.random() > 0.4 else None
        tipo_atendimento = random.choice(TIPOS_ATENDIMENTO)

        # Especialidade baseada no procedimento/CID
        if procedimento and ("FACO" in procedimento or "LIO" in procedimento or "FACECTOMIA" in procedimento):
            especialidade = "Catarata e Cirurgia Refrativa"
        elif tipo_atendimento == "Retorno Ambulatorial" or cid == "Z54.0":
            especialidade = "Pós-Operatório / Retorno"
        elif cid and (cid.startswith("H16") or cid.startswith("H18")):
            especialidade = "Córnea e Doenças Externas"
        elif cid and (cid.startswith("H35") or cid.startswith("H43") or (procedimento and "VITRECTOMIA" in procedimento)):
            especialidade = "Retina e Vítreo"
        elif cid and cid.startswith("H40"):
            especialidade = "Glaucoma"
        else:
            especialidade = random.choice(ESPECIALIDADES)

        # Motivo Clínico
        if procedimento:
            motivo_clinico = f"Indicação clínica para {procedimento}"
        elif cid:
            motivo_clinico = f"Atendimento oftalmológico especializado para CID {cid}"
        else:
            motivo_clinico = f"Avaliação de saúde ocular - {tipo_atendimento}"

        canal_origem = random.choice(CANAIS)
        prof_id = random.randint(1, len(medicos_nomes))

        # Lógica de status e agendamentos baseada na data
        if dt_atend < datetime(2025, 6, 1):
            # Atendimentos antigos: encerrados
            status = "ENCERRADA"
            dt_solic = dt_atend - timedelta(days=random.randint(10, 30))
            dt_atualizacao = dt_atend
            dt_encerra = dt_agendada.strftime("%Y-%m-%d %H:%M:%S")

            agendamentos_rows.append((
                agendamento_id_seq, aid, prof_id,
                dt_agendada.strftime("%Y-%m-%d %H:%M:%S"),
                "REALIZADO", "CONFIRMADO",
                dt_agendada.strftime("%Y-%m-%d %H:%M:%S"),
                dt_solic.strftime("%Y-%m-%d %H:%M:%S"),
                dt_atend.strftime("%Y-%m-%d %H:%M:%S")
            ))
            agendamento_id_seq += 1

            historico_rows.append((
                historico_id_seq, aid, 1, "AGENDADA", "ENCERRADA",
                dt_atend.strftime("%Y-%m-%d %H:%M:%S")
            ))
            historico_id_seq += 1

        else:
            # Atendimentos recentes: status variados para o painel
            mod = aid % 10
            if mod in (0, 1, 2, 3, 4):  # 50% Agendadas
                status = "AGENDADA"
                dt_solic = dt_atend - timedelta(days=random.randint(5, 20))
                dt_atualizacao = dt_atend - timedelta(days=random.randint(0, 5))
                dt_encerra = None

                agendamentos_rows.append((
                    agendamento_id_seq, aid, prof_id,
                    dt_agendada.strftime("%Y-%m-%d %H:%M:%S"),
                    "AGENDADO", "CONFIRMADO",
                    None,
                    dt_solic.strftime("%Y-%m-%d %H:%M:%S"),
                    dt_atualizacao.strftime("%Y-%m-%d %H:%M:%S")
                ))
                agendamento_id_seq += 1

                historico_rows.append((
                    historico_id_seq, aid, 1, "EM_TRIAGEM", "AGENDADA",
                    dt_atualizacao.strftime("%Y-%m-%d %H:%M:%S")
                ))
                historico_id_seq += 1

            elif mod in (5, 6):  # 20% Em Triagem
                status = "EM_TRIAGEM"
                dt_solic = dt_atend - timedelta(days=random.randint(2, 10))
                dt_atualizacao = dt_atend - timedelta(days=random.randint(0, 3))
                dt_encerra = None

                historico_rows.append((
                    historico_id_seq, aid, 1, "RECEBIDA", "EM_TRIAGEM",
                    dt_atualizacao.strftime("%Y-%m-%d %H:%M:%S")
                ))
                historico_id_seq += 1

            elif mod in (7, 8):  # 20% Aguardando Vaga
                status = "AGUARDANDO"
                dt_solic = dt_atend - timedelta(days=random.randint(5, 15))
                dt_atualizacao = dt_atend - timedelta(days=random.randint(1, 7))
                dt_encerra = None

                historico_rows.append((
                    historico_id_seq, aid, 1, "RECEBIDA", "AGUARDANDO",
                    dt_atualizacao.strftime("%Y-%m-%d %H:%M:%S")
                ))
                historico_id_seq += 1

            else:  # 10% Recebida
                status = "RECEBIDA"
                dt_solic = dt_atend - timedelta(days=random.randint(0, 5))
                dt_atualizacao = dt_solic
                dt_encerra = None

                historico_rows.append((
                    historico_id_seq, aid, 1, None, "RECEBIDA",
                    dt_solic.strftime("%Y-%m-%d %H:%M:%S")
                ))
                historico_id_seq += 1

        solicitacoes_rows.append((
            aid, protocolo, pid, prioridade, possui_pedido_medico, cid, motivo_clinico,
            tipo_atendimento, especialidade, procedimento, canal_origem, status,
            dt_solic.strftime("%Y-%m-%d %H:%M:%S"),
            dt_atualizacao.strftime("%Y-%m-%d %H:%M:%S"),
            dt_encerra
        ))

    cur.executemany("""
    INSERT INTO solicitacoes_atendimento (
        id, protocolo, paciente_id, prioridade, possui_pedido_medico, cid, motivo_clinico,
        tipo_atendimento, especialidade, procedimento, canal_origem, status,
        data_solicitacao, data_atualizacao, data_encerramento
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, solicitacoes_rows)
    print(f"[OK] {len(solicitacoes_rows)} Solicitações de atendimento fictícias inseridas.")

    cur.executemany("""
    INSERT INTO agendamentos (
        id, solicitacao_id, profissional_id, data_agendada, status, status_confirmacao,
        data_realizacao, data_cadastro, data_atualizacao
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, agendamentos_rows)
    print(f"[OK] {len(agendamentos_rows)} Agendamentos fictícios inseridos.")

    cur.executemany("""
    INSERT INTO historico_solicitacoes (
        id, solicitacao_id, usuario_id, status_anterior, novo_status, data_alteracao
    ) VALUES (?, ?, ?, ?, ?, ?)
    """, historico_rows)
    print(f"[OK] {len(historico_rows)} Entradas de histórico fictícias inseridas.")

    # Cria índices para consultas ultrarrápidas
    cur.execute("CREATE INDEX IF NOT EXISTS idx_solicitacoes_protocolo ON solicitacoes_atendimento(protocolo)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_solicitacoes_paciente ON solicitacoes_atendimento(paciente_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_solicitacoes_status ON solicitacoes_atendimento(status)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_pacientes_cpf ON pacientes(cpf)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_pacientes_cns ON pacientes(cns)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_agendamentos_solicitacao ON agendamentos(solicitacao_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_agendamentos_profissional ON agendamentos(profissional_id)")

    con.commit()
    con.close()
    print("Banco de dados do BOS populado com sucesso com DADOS FICTÍCIOS!")
    print(f"Total: {NUM_PACIENTES} pacientes, {len(medicos_nomes)} profissionais, {NUM_SOLICITACOES} solicitações, {len(agendamentos_rows)} agendamentos")

if __name__ == "__main__":
    popular_banco()