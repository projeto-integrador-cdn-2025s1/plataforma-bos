import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# Configuração de alta resolução e dimensões widescreen
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

fig, ax = plt.subplots(figsize=(16, 8.5), dpi=300)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# 1. Título e Subtítulo
ax.text(0.8, 8.2, "FLUXO DE USO DA PLATAFORMA BOS", fontsize=18, fontweight='bold', color='#0f2d4a', va='center')
ax.text(0.8, 7.7, "JORNADA DO PACIENTE SUS & SISTEMA DE GESTÃO INTEGRADA — PROCESSO DE CATARATA", fontsize=11, fontweight='semibold', color='#52799c', va='center')

# Cores da paleta institucional BOS / Saúde
c_step_bg = '#f1f5f9'
c_step_border = '#64748b'
c_step_text = '#0f172a'

c_final_bg = '#cbd5e1'
c_final_border = '#334155'
c_final_text = '#0f172a'

c_mod_bg = '#e2e8f0'
c_mod_border = '#475569'
c_mod_text = '#1e293b'

# 2. Definição das 6 etapas superiores da Jornada
top_boxes = [
    {
        "title": "Consulta e\nAvaliação Inicial",
        "sub": "Acolhimento UBS / BOS\ne triagem clínica",
        "x": 0.8, "w": 2.0, "h": 2.1,
        "bg": c_step_bg, "border": c_step_border, "text": c_step_text
    },
    {
        "title": "Exames\nPré-operatórios",
        "sub": "Biometria, mapeamento\ne acuidade visual",
        "x": 3.25, "w": 2.0, "h": 2.1,
        "bg": c_step_bg, "border": c_step_border, "text": c_step_text
    },
    {
        "title": "Avaliação Pré-op.\ne Agendamento",
        "sub": "Definição de data,\nhorário e cirurgião",
        "x": 5.7, "w": 2.0, "h": 2.1,
        "bg": c_step_bg, "border": c_step_border, "text": c_step_text
    },
    {
        "title": "Procedimento\nCirúrgico",
        "sub": "Facoemulsificação com\nimplante de LIO",
        "x": 8.15, "w": 2.0, "h": 2.1,
        "bg": c_step_bg, "border": c_step_border, "text": c_step_text
    },
    {
        "title": "Acompanhamento\nPós-operatório",
        "sub": "Consultas de retorno e\nrecuperação visual",
        "x": 10.6, "w": 2.0, "h": 2.1,
        "bg": c_step_bg, "border": c_step_border, "text": c_step_text
    },
    {
        "title": "Análise, Regulação\ne Decisão (Gestão)",
        "sub": "Monitoramento de filas\ne eficiência do SUS",
        "x": 13.05, "w": 2.15, "h": 2.1,
        "bg": c_final_bg, "border": c_final_border, "text": c_final_text, "bold": True
    }
]

y_top = 4.7

# Desenha os cards superiores
for i, b in enumerate(top_boxes):
    box = patches.FancyBboxPatch(
        (b["x"], y_top), b["w"], b["h"],
        boxstyle="round,pad=0.1,rounding_size=0.18",
        linewidth=1.8, edgecolor=b["border"], facecolor=b["bg"]
    )
    ax.add_patch(box)
    
    # Texto
    center_x = b["x"] + b["w"] / 2
    center_y = y_top + b["h"] / 2 + 0.15
    ax.text(center_x, center_y, b["title"], ha='center', va='center',
            fontsize=10.5, fontweight='bold' if b.get('bold') else 'semibold', color=b["text"], linespacing=1.2)
    ax.text(center_x, y_top + 0.45, b["sub"], ha='center', va='center',
            fontsize=8.5, color='#475569', linespacing=1.2)

    # Setas horizontais entre cards superiores
    if i < len(top_boxes) - 1:
        arrow_x1 = b["x"] + b["w"] + 0.08
        arrow_x2 = top_boxes[i+1]["x"] - 0.08
        arrow_y = y_top + b["h"] / 2
        ax.annotate(
            '', xy=(arrow_x2, arrow_y), xytext=(arrow_x1, arrow_y),
            arrowprops=dict(arrowstyle="-|>", color="#475569", lw=2.2, mutation_scale=16)
        )

# 3. Definição dos 3 Módulos Inferiores da Plataforma
bottom_boxes = [
    {
        "title": "Chatbot & Orientação ao Paciente",
        "desc": "Assistente virtual para esclarecimento de dúvidas frequentes,\nrequisitos regulatórios, orientações pré/pós e preparo cirúrgico.",
        "x": 0.8, "w": 4.45, "h": 1.7,
        "targets": [0.8 + 2.0/2, 3.25 + 2.0/2]
    },
    {
        "title": "Módulo de Consulta Pública & Base Integrada",
        "desc": "Acompanhamento transparente por código/protocolo BOS ou CPF,\nintegração com prontuário (MV/CROSS) e atualização em tempo real.",
        "x": 5.7, "w": 4.45, "h": 1.7,
        "targets": [5.7 + 2.0/2, 8.15 + 2.0/2]
    },
    {
        "title": "Painel Gerencial e BI de Atendimento",
        "desc": "Dashboard com 14.000+ atendimentos: acompanhamento por médico,\nfilas de espera, distribuição por município DRS XVI e prioridades SUS.",
        "x": 10.6, "w": 4.6, "h": 1.7,
        "targets": [10.6 + 2.0/2, 13.05 + 2.15/2]
    }
]

y_bottom = 1.3

for m in bottom_boxes:
    # Card do módulo
    box = patches.FancyBboxPatch(
        (m["x"], y_bottom), m["w"], m["h"],
        boxstyle="round,pad=0.1,rounding_size=0.18",
        linewidth=1.8, edgecolor=c_mod_border, facecolor=c_mod_bg
    )
    ax.add_patch(box)

    cx = m["x"] + m["w"] / 2
    ax.text(cx, y_bottom + m["h"] - 0.45, m["title"], ha='center', va='center',
            fontsize=11, fontweight='bold', color=c_mod_text)
    ax.text(cx, y_bottom + 0.55, m["desc"], ha='center', va='center',
            fontsize=8.5, color='#334155', linespacing=1.25)

    # Setas verticais apontando para os cards superiores
    for tx in m["targets"]:
        ax.annotate(
            '', xy=(tx, y_top - 0.08), xytext=(tx, y_bottom + m["h"] + 0.08),
            arrowprops=dict(arrowstyle="-|>", color="#475569", lw=2.2, mutation_scale=16)
        )

# Linha sutil de rodapé
ax.plot([0.8, 15.2], [0.55, 0.55], color='#cbd5e1', lw=1)
ax.text(0.8, 0.35, "Plataforma BOS — Banco de Olhos de Sorocaba | Referência em Saúde Ocular SUS", fontsize=8.5, color='#64748b', va='center')
ax.text(15.2, 0.35, "Tecnologia Aplicada à Fila e Gestão de Catarata", fontsize=8.5, color='#64748b', ha='right', va='center')

plt.subplots_adjust(left=0.03, right=0.97, top=0.95, bottom=0.05)

# Salva na pasta do projeto e no diretório de artefatos
out_project = Path(r"C:\Users\Marco\Desktop\lo-files\computher showt\plataforma-bos\fluxo_jornada_paciente.png")
out_brain = Path(r"C:\Users\Marco\.gemini\antigravity\brain\42d0f7f9-bcc7-4184-a804-8c96eefd40aa\fluxo_jornada_paciente.png")

fig.savefig(out_project, format='png', dpi=300, bbox_inches='tight')
fig.savefig(out_brain, format='png', dpi=300, bbox_inches='tight')

print(f"Imagem gerada com sucesso em:\n{out_project}\n{out_brain}")
