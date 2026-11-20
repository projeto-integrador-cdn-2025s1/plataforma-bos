import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')
ax.set_xlim(0, 16)
ax.set_ylim(0, 9.5)
ax.axis('off')

# 1. Título e Subtítulo
ax.text(0.8, 8.85, "FIGURA 3 — CAMADAS DA ARQUITETURA DO SISTEMA", 
        fontsize=16, fontweight='bold', color='#0f2d4a', va='center')
ax.text(0.8, 8.4, "ARQUITETURA EM 4 CAMADAS MODULARES — PLATAFORMA BOS (GESTÃO & ORIENTAÇÃO SUS)", 
        fontsize=10.5, fontweight='bold', color='#52799c', va='center')

# Cores por camada
layers = [
    {
        "num": "CAMADA 1: USO / APRESENTAÇÃO (FRONTEND)",
        "tech": "HTML5, CSS3, Bootstrap 5, Chart.js / Streamlit",
        "color_header": "#1e3a8a",
        "color_bg": "#eff6ff",
        "color_border": "#3b82f6",
        "y": 6.35, "h": 1.7,
        "boxes": [
            ("Portal Público do Paciente", "Consulta de situação por protocolo ou CPF;\nAcompanhamento das etapas do fluxo SUS;\nInterface responsiva para celular e desktop.", 1.2, 4.2),
            ("Assistente Virtual (Chatbot)", "Interface interativa de perguntas e respostas;\nOrientação 24/7 sobre preparo cirúrgico,\nexames, documentos e regras do CROSS.", 5.7, 4.3),
            ("Dashboard Gerencial (BI)", "Painel analítico para a equipe do BOS;\nFiltros por status, médico, prioridade e cidade;\nMétricas consolidadas de 14.000+ atendimentos.", 10.3, 4.5)
        ]
    },
    {
        "num": "CAMADA 2: SERVIÇO / APLICAÇÃO (BACKEND)",
        "tech": "Python, Flask, Jinja2, Controladores e Regras de Negócio",
        "color_header": "#0369a1",
        "color_bg": "#f0f9ff",
        "color_border": "#0284c7",
        "y": 4.35, "h": 1.6,
        "boxes": [
            ("Módulo de Consulta & Segurança", "Validação de protocolo e CPF mascarado;\nControle de sessão e autenticação de usuários\npor perfil (Administrador e Atendimento).", 1.2, 4.2),
            ("Motor de Processamento do Chatbot", "Mapeamento semântico de dúvidas frequentes;\nBusca estrita na base homologada pelo BOS;\nRespostas seguras (sem alucinações médicas).", 5.7, 4.3),
            ("Motor de Agregação Analítica", "Cálculo em tempo real de KPIs de fila SUS;\nClassificação automática de prioridades (P1-P4);\nNormalização toponímica dos 48 municípios.", 10.3, 4.5)
        ]
    },
    {
        "num": "CAMADA 3: PERSISTÊNCIA / DADOS (STORAGE)",
        "tech": "Banco de Dados Relacional (SQLite / SQLAlchemy ORM)",
        "color_header": "#0f766e",
        "color_bg": "#f0fdfa",
        "color_border": "#0d9488",
        "y": 2.45, "h": 1.5,
        "boxes": [
            ("Tabela: pacientes", "Identificação, nascimento,\ncontato, endereço e município.", 1.2, 3.2),
            ("Tabela: profissionais", "120 médicos oftalmologistas\ne corpo clínico credenciado.", 4.7, 3.2),
            ("Tabela: solicitacoes_atendimento", "Protocolos BOS, CIDs, procedimentos,\nprioridades e status da fila SUS.", 8.2, 3.6),
            ("Tabela: agendamentos & FAQ", "Datas de cirurgias, confirmações,\nhistórico e base de conhecimento.", 12.1, 2.7)
        ]
    },
    {
        "num": "CAMADA 4: INTEGRAÇÕES EXTERNAS (DATA SOURCES)",
        "tech": "Exportações Tabulares do Sistema MV & Conexões Regulatórias SUS",
        "color_header": "#334155",
        "color_bg": "#f8fafc",
        "color_border": "#64748b",
        "y": 0.85, "h": 1.2,
        "boxes": [
            ("Sistema MV Hospitalar", "Exportações de prontuário eletrônico, cirurgias e consultas de catarata.", 1.2, 6.5),
            ("Regulação Estadual CROSS / UBS", "Pactuações intermunicipais e encaminhamentos da DRS XVI.", 8.0, 6.8)
        ]
    }
]

# Renderização das camadas
for layer in layers:
    y = layer["y"]
    h = layer["h"]
    
    # Fundo do container da camada
    c_box = patches.FancyBboxPatch((0.8, y), 14.4, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                                   linewidth=1.8, edgecolor=layer["color_border"], facecolor=layer["color_bg"])
    ax.add_patch(c_box)
    
    # Faixa lateral do nome da camada
    lbl_box = patches.FancyBboxPatch((0.8, y + h - 0.38), 14.4, 0.38, boxstyle="round,pad=0.04,rounding_size=0.12",
                                     linewidth=0, facecolor=layer["color_header"])
    ax.add_patch(lbl_box)
    
    ax.text(1.0, y + h - 0.19, layer["num"], fontsize=9.5, fontweight='bold', color='#FFFFFF', va='center')
    ax.text(15.0, y + h - 0.19, f"Tecnologias: {layer['tech']}", fontsize=8.0, color='#e2e8f0', ha='right', va='center')
    
    # Componentes internos
    for b_title, b_desc, bx, bw in layer["boxes"]:
        inner_y = y + 0.12
        inner_h = h - 0.58
        ibox = patches.FancyBboxPatch((bx, inner_y), bw, inner_h, boxstyle="round,pad=0.04,rounding_size=0.08",
                                      linewidth=1.0, edgecolor=layer["color_border"], facecolor='#FFFFFF')
        ax.add_patch(ibox)
        ax.text(bx + bw/2, inner_y + inner_h - 0.25, b_title, fontsize=8.8, fontweight='bold', color=layer["color_header"], ha='center', va='center')
        ax.text(bx + bw/2, inner_y + (inner_h - 0.25)/2, b_desc, fontsize=7.2, color='#334155', ha='center', va='center', linespacing=1.2)

# Setas verticais bidirecionais entre as camadas
arrow_xs = [3.2, 7.8, 12.5]

for ax_pos in arrow_xs:
    # Camada 1 <-> Camada 2
    ax.annotate('', xy=(ax_pos, 6.35), xytext=(ax_pos, 5.95),
                arrowprops=dict(arrowstyle="<->", color="#0284c7", lw=2.0, mutation_scale=14))
    # Camada 2 <-> Camada 3
    ax.annotate('', xy=(ax_pos, 4.35), xytext=(ax_pos, 3.95),
                arrowprops=dict(arrowstyle="<->", color="#0d9488", lw=2.0, mutation_scale=14))
    # Camada 3 <-> Camada 4
    ax.annotate('', xy=(ax_pos, 2.45), xytext=(ax_pos, 2.05),
                arrowprops=dict(arrowstyle="<->", color="#64748b", lw=2.0, mutation_scale=14))

# Rodapé ABNT
ax.plot([0.8, 15.2], [0.55, 0.55], color='#cbd5e1', lw=1)
ax.text(0.8, 0.32, "Fonte: elaborado pelos autores (2026).", fontsize=8.5, color='#475569', style='italic', va='center')
ax.text(15.2, 0.32, "Arquitetura Modular Baseada na Tabela 10 — Banco de Olhos de Sorocaba", fontsize=8.5, color='#64748b', ha='right', va='center')

plt.subplots_adjust(left=0.03, right=0.97, top=0.96, bottom=0.04)

out_project = Path(r"C:\Users\Marco\Desktop\lo-files\computher showt\plataforma-bos\figura3_camadas_arquitetura.png")
out_brain = Path(r"C:\Users\Marco\.gemini\antigravity\brain\42d0f7f9-bcc7-4184-a804-8c96eefd40aa\figura3_camadas_arquitetura.png")

fig.savefig(out_project, format='png', dpi=300, bbox_inches='tight')
fig.savefig(out_brain, format='png', dpi=300, bbox_inches='tight')

print(f"Figura 3 gerada com sucesso em:\n{out_project}\n{out_brain}")
