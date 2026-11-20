#!/usr/bin/env python3
"""
Gera README_PLATAFORMA_BOS.pdf — guia rápido de configuração, inicialização e manutenção.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ─── Estilos ───
styles = getSampleStyleSheet()
COR_PRIMARIA = HexColor("#1B4F72")
COR_SECUNDARIA = HexColor("#2E86C1")
COR_FUNDO = HexColor("#F8F9FA")
COR_TEXTO = HexColor("#2C3E50")

styles.add(ParagraphStyle(
    'TituloPrincipal', parent=styles['Title'],
    fontSize=22, leading=26, textColor=COR_PRIMARIA, spaceAfter=6,
    alignment=TA_CENTER, fontName='Helvetica-Bold'
))
styles.add(ParagraphStyle(
    'SubTitulo', parent=styles['Heading1'],
    fontSize=16, leading=20, textColor=COR_SECUNDARIA, spaceBefore=12, spaceAfter=6,
    fontName='Helvetica-Bold'
))
styles.add(ParagraphStyle(
    'Secao', parent=styles['Heading2'],
    fontSize=13, leading=16, textColor=COR_PRIMARIA, spaceBefore=10, spaceAfter=4,
    fontName='Helvetica-Bold'
))
styles.add(ParagraphStyle(
    'Corpo', parent=styles['Normal'],
    fontSize=10, leading=13, textColor=COR_TEXTO, spaceAfter=4,
    fontName='Helvetica'
))
styles.add(ParagraphStyle(
    'Codigo', parent=styles['Code'],
    fontSize=9, leading=11, textColor=HexColor("#1A1A2E"),
    backColor=COR_FUNDO, borderPadding=6, fontName='Courier',
    spaceBefore=4, spaceAfter=4
))
styles.add(ParagraphStyle(
    'ItemLista', parent=styles['Normal'],
    fontSize=10, leading=13, textColor=COR_TEXTO, leftIndent=18,
    bulletIndent=6, spaceAfter=2, fontName='Helvetica'
))
styles.add(ParagraphStyle(
    'Rodape', parent=styles['Normal'],
    fontSize=8, leading=10, textColor=HexColor("#7F8C8D"),
    alignment=TA_CENTER, fontName='Helvetica-Oblique'
))

# ─── Conteúdo ───
story = []

# ── Capa ──
story.append(Spacer(1, 2.5*cm))

# Linha decorativa superior
story.append(Paragraph(
    '<para alignment="center"><font color="#1B4F72" size="2">━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</font></para>',
    styles['Corpo']
))
story.append(Spacer(1, 0.8*cm))

story.append(Paragraph("PLATAFORMA BOS", styles['TituloPrincipal']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    '<para alignment="center"><font color="#2E86C1" size="14"><b>Banco de Olhos de Sorocaba</b></font></para>',
    styles['Corpo']
))
story.append(Spacer(1, 1.2*cm))

# Subtítulo com fundo sutil
story.append(Paragraph(
    '<para alignment="center" backColor="#F0F4F8" borderPadding="10">'
    '<font color="#1B4F72" size="12"><b>Guia de Configuração, Inicialização e Manutenção</b></font>'
    '</para>',
    styles['Corpo']
))
story.append(Spacer(1, 2*cm))

# Linha decorativa inferior
story.append(Paragraph(
    '<para alignment="center"><font color="#1B4F72" size="2">━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</font></para>',
    styles['Corpo']
))
story.append(Spacer(1, 2.5*cm))

# Bloco de informações institucionais
info_inst = [
    ["Versão", "1.0"],
    ["Data", "Novembro 2026"],
    ["Instituição Parceira", "FATEC Votorantim"],
    ["Instituição Executora", "Banco de Olhos de Sorocaba (BOS)"],
    ["Projeto", "Plataforma de Gestão do Fluxo de Catarata SUS"],
    ["Classificação", "Uso Interno — Governança LGPD"],
]
t_capa = Table(info_inst, colWidths=[5.5*cm, 10*cm])
t_capa.setStyle(TableStyle([
    ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('TEXTCOLOR', (0,0), (-1,-1), COR_TEXTO),
    ('TEXTCOLOR', (0,0), (0,-1), COR_PRIMARIA),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LINEBELOW', (0,0), (-1,-2), 0.5, HexColor("#D5D8DC")),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_capa)

story.append(Spacer(1, 2*cm))
story.append(Paragraph(
    '<para alignment="center"><font color="#7F8C8D" size="9">'
    'Documento técnico de apoio à implantação e operação da plataforma.<br/>'
    'Contato: sus@bos.org.br | (15) 3212-7000 ramal 03'
    '</font></para>',
    styles['Corpo']
))
story.append(PageBreak())

# ── 1. Visão Geral ──
story.append(Paragraph("1. Visão Geral", styles['Secao']))
story.append(Paragraph(
    "Plataforma web em <b>Flask + SQLAlchemy + SQLite</b> para gestão do fluxo de catarata SUS. "
    "Oferece: consulta pública por protocolo/CPF, assistente virtual (chatbot híbrido Gemini/local), "
    "e painel gerencial com KPIs, gráficos e gestão de status de solicitações.",
    styles['Corpo']
))

# ── 2. Pré-requisitos ──
story.append(Paragraph("2. Pré-requisitos", styles['Secao']))
reqs = [
    "Python 3.10+",
    "pip atualizado",
    "Git (opcional, para versionamento)",
    "Acesso à internet (para instalar dependências e usar Gemini API)",
]
for r in reqs:
    story.append(Paragraph(f"- {r}", styles['ItemLista']))

# ── 3. Instalação e Configuração ──
story.append(Paragraph("3. Instalação e Configuração", styles['Secao']))

story.append(Paragraph("<b>3.1 Clonar / preparar o projeto</b>", styles['Corpo']))
story.append(Paragraph("Se já tem a pasta, pule para 3.2. Caso contrário:", styles['Corpo']))
story.append(Paragraph("git clone <repo> plataforma-bos && cd plataforma-bos", styles['Codigo']))

story.append(Paragraph("<b>3.2 Ambiente virtual e dependências</b>", styles['Corpo']))
story.append(Paragraph("python -m venv .venv && source .venv/bin/activate  # Linux/Mac", styles['Codigo']))
story.append(Paragraph(".venv\\Scripts\\activate  # Windows", styles['Codigo']))
story.append(Paragraph("pip install -r requirements.txt", styles['Codigo']))

story.append(Paragraph("<b>3.3 Variáveis de ambiente (.env)</b>", styles['Corpo']))
story.append(Paragraph("Crie <b>.env</b> na raiz com:", styles['Corpo']))
env_exemplo = (
    "SECRET_KEY=bos_chave_secreta_atendimento_sus_2026\n"
    "OLLAMA_API_KEY=sua_chave_ollama\n"
    "GEMINI_API_KEY=sua_chave_gemini  # opcional: ativa camada 1 do chatbot"
)
story.append(Paragraph(env_exemplo, styles['Codigo']))
story.append(Paragraph(
    "Sem <b>GEMINI_API_KEY</b> o chatbot usa fallback local (base_info.txt). "
    "O <b>SECRET_KEY</b> protege sessões Flask; altere em produção.",
    styles['Corpo']
))

# ── 4. Inicialização ──
story.append(Paragraph("4. Inicialização", styles['Secao']))
story.append(Paragraph("<b>4.1 Popular o banco (primeira vez)</b>", styles['Corpo']))
story.append(Paragraph("python seed_db.py", styles['Codigo']))
story.append(Paragraph(
    "Lê <b>data/PROJETO_FATEC_CATARATA.csv</b> e cria <b>instance/bos.db</b> com "
    "7.650 pacientes, 14.068 solicitações, 13.711 agendamentos, 120 profissionais e 2 usuários.",
    styles['Corpo']
))

story.append(Paragraph("<b>4.2 Rodar a aplicação</b>", styles['Corpo']))
story.append(Paragraph("python main.py", styles['Codigo']))
story.append(Paragraph(
    "Sobe em <b>http://0.0.0.0:5000</b> (debug=True). Acesse no navegador.",
    styles['Corpo']
))

story.append(Paragraph("<b>4.3 Credenciais padrão do painel</b>", styles['Corpo']))
tabela_cred = Table([
    ["Perfil", "E-mail", "Senha"],
    ["Atendimento", "atendimento@bos.org.br", "bos123"],
    ["Administrador", "admin@bos.org.br", "admin123"],
], colWidths=[3.5*cm, 6*cm, 4*cm])
tabela_cred.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), COR_PRIMARIA),
    ('TEXTCOLOR', (0,0), (-1,0), HexColor("#FFFFFF")),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('GRID', (0,0), (-1,-1), 0.5, HexColor("#CCCCCC")),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor("#FFFFFF"), COR_FUNDO]),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(tabela_cred)
story.append(Spacer(1, 6))

# ── 5. Estrutura de Pastas ──
story.append(Paragraph("5. Estrutura Principal", styles['Secao']))
estrutura = """
plataforma-bos/
+-- app/                    # Pacote Flask
|   +-- __init__.py         # Factory iniciar()
|   +-- models.py           # 6 modelos SQLAlchemy
|   +-- extensions.py       # db = SQLAlchemy()
|   +-- model/
|   |   +-- base_info.txt   # Contexto do chatbot (fallback)
|   |   +-- chat.py         # Logica Gemini + fallback
|   +-- templates/          # 7 templates HTML (Bootstrap 5)
+-- controllers/
|   +-- general_controllers.py  # Logica de rotas
+-- routes/
|   +-- general.py          # Blueprints
+-- data/
|   +-- PROJETO_FATEC_CATARATA.csv  # Fonte de seed
+-- instance/
|   +-- bos.db              # SQLite (criado pelo seed)
+-- scripts/                # Geracao de diagramas (figuras)
+-- docs/                   # PDFs de apoio (guia, dicionario, PDCA)
+-- seed_db.py              # ETL + povoamento
+-- main.py                 # Entry point
+-- requirements.txt
+-- .env                    # Segredos (nao versionar)
+-- test_app.py             # Testes unittest
"""
story.append(Paragraph(estrutura.replace('\n', '<br/>'), styles['Codigo']))

# ── 6. Manutenção do Banco de Dados ──
story.append(Paragraph("6. Manutenção do Banco de Dados", styles['Secao']))

story.append(Paragraph("<b>6.1 Backup</b>", styles['Corpo']))
story.append(Paragraph("cp instance/bos.db instance/bos_$(date +%F).db", styles['Codigo']))
story.append(Paragraph("Faça backup <b>diário</b> em produção. O arquivo é leve (~50 MB).", styles['Corpo']))

story.append(Paragraph("<b>6.2 Recriar / re-povoar</b>", styles['Corpo']))
story.append(Paragraph("rm instance/bos.db && python seed_db.py", styles['Codigo']))
story.append(Paragraph("Apaga e recria tabelas + dados do CSV. Útil após mudança de schema.", styles['Corpo']))

story.append(Paragraph("<b>6.3 Migração de schema (futuro)</b>", styles['Corpo']))
story.append(Paragraph(
    "Hoje usa <b>db.create_all()</b> (linha 17 de app/__init__.py). Para evoluir sem perda de dados, "
    "adote <b>Flask-Migrate (Alembic)</b>: pip install flask-migrate && flask db init && flask db migrate -m \"msg\" && flask db upgrade.",
    styles['Corpo']
))

story.append(Paragraph("<b>6.4 Índices úteis (já criados no seed)</b>", styles['Corpo']))
idx = [
    "idx_solicitacoes_protocolo  — busca por protocolo",
    "idx_solicitacoes_paciente   — join paciente→solicitações",
    "idx_solicitacoes_status     — filtros de status no painel",
    "idx_pacientes_cpf / cns     — consulta pública por CPF/CNS",
    "idx_agendamentos_solicitacao / profissional",
]
for i in idx:
    story.append(Paragraph(f"- {i}", styles['ItemLista']))

# ── 7. Manutenção dos Módulos ──
story.append(Paragraph("7. Manutenção dos Módulos", styles['Secao']))

mods = [
    ("Chatbot (app/model/chat.py)",
     "• Edite <b>base_info.txt</b> para atualizar respostas do fallback local.<br/>"
     "• Troque <b>GEMINI_API_KEY</b> no .env para mudar a chave.<br/>"
     "• Modelo padrão: <b>gemini-1.5-flash</b> (linha 63)."),
    ("Painel Gerencial (controllers/general_controllers.py + templates/painel.html)",
     "• KPIs: função <b>get_painel()</b> — agregações SQL ultrarrápidas.<br/>"
     "• Gráficos: Chart.js (via CDN) alimentado por JSON no template.<br/>"
     "• Filtros: JS puro no template (busca + select status)."),
    ("Consulta Pública (routes/general.py → /consulta)",
     "• Busca por protocolo, CPF ou CNS.<br/>"
     "• Mascaramento de CPF/nome no template (funções em controllers)."),
    ("Modelos (app/models.py)",
     "• 6 tabelas com <b>CheckConstraints</b> para integridade.<br/>"
     "• Relacionamentos: paciente↔solicitações↔agendamentos↔profissionais + histórico.<br/>"
     "• Propriedade <b>tempo_espera_dias</b> calculada dinamicamente."),
    ("Seed / ETL (seed_db.py)",
     "• Pipeline completo: limpeza de endereços, normalização de municípios (DRS XVI), "
     "deduplicação CPF/CNS, geração de protocolos BOS-XXXXX.<br/>"
     "• Atualize <b>MUNICIPIOS_REGIAO_SOROCABA</b> se a lista mudar."),
]
for titulo, desc in mods:
    story.append(Paragraph(f"<b>{titulo}</b>", styles['Corpo']))
    story.append(Paragraph(desc, styles['Corpo']))

# ── 8. Rotinas Recomendadas ──
story.append(Paragraph("8. Rotinas Recomendadas", styles['Secao']))
rotinas = [
    ("Diária", "Backup do bos.db; verificar logs de erro no console."),
    ("Semanal", "Rodar <b>python test_app.py</b> (suite unittest); checar espaço em disco."),
    ("Mensal", "Revisar KPIs no painel: tempo médio de espera, % em triagem, assertividade do chatbot (KPI 3 ≥ 80%)."),
    ("Por demanda", "Atualizar <b>base_info.txt</b> quando houver mudança de procedimento/contato no BOS; "
                    "repopular banco se CSV de origem for atualizado."),
]
for freq, desc in rotinas:
    story.append(Paragraph(f"<b>{freq}:</b> {desc}", styles['ItemLista']))

# ── 9. Troubleshooting Rápido ──
story.append(Paragraph("9. Troubleshooting Rápido", styles['Secao']))
problemas = [
    ("ModuleNotFoundError", "Ative o venv e rode <b>pip install -r requirements.txt</b>."),
    ("sqlite3.OperationalError: no such table", "Banco não criado: rode <b>python seed_db.py</b>."),
    ("Chatbot não responde", "Verifique <b>GEMINI_API_KEY</b> no .env; sem ela usa fallback local."),
    ("Erro de encoding no CSV", "seed_db.py abre com <b>utf-8-sig</b> e errors='replace'."),
    ("Porta 5000 ocupada", "Altere em main.py: <b>app.run(port=5001)</b> ou mate o processo."),
    ("Templates não atualizam", "Flask em debug recarrega auto; force Ctrl+F5 no navegador."),
]
for prob, sol in problemas:
    story.append(Paragraph(f"<b>{prob}:</b> {sol}", styles['ItemLista']))

# ── 10. Segurança e LGPD ──
story.append(Paragraph("10. Segurança e LGPD (Resumo)", styles['Secao']))
story.append(Paragraph(
    "• Senhas: hash SHA-256 + salt (Werkzeug).<br/>"
    "• CPF/CNS mascarados na interface pública.<br/>"
    "• Consulta prioritária por protocolo (não expõe dados clínicos).<br/>"
    "• Auditoria completa em <b>historico_solicitacoes</b> (quem, quando, o quê).<br/>"
    "• <b>.env</b> NÃO versionar — adicione ao .gitignore.<br/>"
    "• Em produção: HTTPS, SECRET_KEY forte, debug=False, WSGI (gunicorn/uWSGI) + proxy reverso (Nginx).",
    styles['Corpo']
))

# ── Rodapé ──
story.append(Spacer(1, 1.5*cm))
story.append(Paragraph(
    "— Fim do Guia Rápido —<br/>"
    "Banco de Olhos de Sorocaba | FATEC Votorantim 2026<br/>"
    "Contato técnico: sus@bos.org.br | (15) 3212-7000 opção 03",
    styles['Rodape']
))

# ─── Build PDF ───
doc = SimpleDocTemplate(
    "README_PLATAFORMA_BOS.pdf",
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=1.8*cm, bottomMargin=1.8*cm,
    title="README Plataforma BOS",
    author="Projeto FATEC + BOS",
)
doc.build(story)
print("✅ README_PLATAFORMA_BOS.pdf gerado com sucesso!")