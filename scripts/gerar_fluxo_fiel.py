import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

fig, ax = plt.subplots(figsize=(16, 7.5), dpi=300)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')
ax.set_xlim(0, 16)
ax.set_ylim(0, 8)
ax.axis('off')

# 1. Título idêntico ao modelo de referência
ax.text(0.8, 7.3, "FLUXO DA JORNADA DO PACIENTE — PROJETO PILOTO: PROCESSO DE CATARATA",
        fontsize=16, fontweight='bold', color='#1e293b', va='center')

# Cores do modelo original
c_step_bg = '#f1f5f9'
c_step_border = '#475569'
c_step_text = '#0f172a'

c_final_bg = '#cbd5e1'
c_final_border = '#334155'
c_final_text = '#0f172a'

c_mod_bg = '#cbd5e1'
c_mod_border = '#475569'
c_mod_text = '#0f172a'

# 2. As 6 etapas superiores
top_boxes = [
    {"text": "Consulta e\navaliação inicial", "x": 0.8, "w": 2.05, "bg": c_step_bg, "bold": False},
    {"text": "Exames\npré-operatórios", "x": 3.25, "w": 2.05, "bg": c_step_bg, "bold": False},
    {"text": "Avaliação pré-op.\ne agendamento", "x": 5.7, "w": 2.05, "bg": c_step_bg, "bold": False},
    {"text": "Cirurgia", "x": 8.15, "w": 2.05, "bg": c_step_bg, "bold": False},
    {"text": "Acompanhamento\npós-operatório", "x": 10.6, "w": 2.05, "bg": c_step_bg, "bold": False},
    {"text": "Análise e decisão\n(gestão)", "x": 13.05, "w": 2.15, "bg": c_final_bg, "bold": True}
]

y_top = 4.2
h_top = 2.0

for i, b in enumerate(top_boxes):
    box = patches.FancyBboxPatch(
        (b["x"], y_top), b["w"], h_top,
        boxstyle="round,pad=0.08,rounding_size=0.18",
        linewidth=1.8, edgecolor=c_step_border, facecolor=b["bg"]
    )
    ax.add_patch(box)

    cx = b["x"] + b["w"] / 2
    cy = y_top + h_top / 2
    ax.text(cx, cy, b["text"], ha='center', va='center',
            fontsize=11.5, fontweight='bold' if b["bold"] else 'normal',
            color=c_step_text, linespacing=1.3)

    # Setas horizontais
    if i < len(top_boxes) - 1:
        arrow_x1 = b["x"] + b["w"] + 0.06
        arrow_x2 = top_boxes[i+1]["x"] - 0.06
        arrow_y = y_top + h_top / 2
        ax.annotate(
            '', xy=(arrow_x2, arrow_y), xytext=(arrow_x1, arrow_y),
            arrowprops=dict(arrowstyle="-|>", color="#475569", lw=2.2, mutation_scale=16)
        )

# 3. Os 3 blocos inferiores do modelo original
bottom_boxes = [
    {
        "title": "Chatbot de atendimento",
        "sub": "(dúvidas frequentes do paciente)",
        "x": 0.8, "w": 4.5, "h": 1.55,
        "targets": [0.8 + 2.05/2, 3.25 + 2.05/2]
    },
    {
        "title": "Sistema MV → base de dados",
        "sub": "consolidada (ETL)",
        "x": 5.7, "w": 4.5, "h": 1.55,
        "targets": [5.7 + 2.05/2, 8.15 + 2.05/2]
    },
    {
        "title": "Dashboard de acompanhamento",
        "sub": "(etapa, médico, indicadores)",
        "x": 10.6, "w": 4.6, "h": 1.55,
        "targets": [10.6 + 2.05/2, 13.05 + 2.15/2]
    }
]

y_bottom = 1.2

for m in bottom_boxes:
    box = patches.FancyBboxPatch(
        (m["x"], y_bottom), m["w"], m["h"],
        boxstyle="round,pad=0.08,rounding_size=0.18",
        linewidth=1.8, edgecolor=c_mod_border, facecolor=c_mod_bg
    )
    ax.add_patch(box)

    cx = m["x"] + m["w"] / 2
    cy = y_bottom + m["h"] / 2
    ax.text(cx, cy + 0.22, m["title"], ha='center', va='center',
            fontsize=12, fontweight='bold', color=c_mod_text)
    ax.text(cx, cy - 0.25, m["sub"], ha='center', va='center',
            fontsize=11, color='#334155')

    # Setas verticais
    for tx in m["targets"]:
        ax.annotate(
            '', xy=(tx, y_top - 0.08), xytext=(tx, y_bottom + m["h"] + 0.08),
            arrowprops=dict(arrowstyle="-|>", color="#475569", lw=2.2, mutation_scale=16)
        )

plt.subplots_adjust(left=0.04, right=0.96, top=0.94, bottom=0.06)

out_project = Path(r"C:\Users\Marco\Desktop\lo-files\computher showt\plataforma-bos\fluxo_jornada_referencia.png")
out_brain = Path(r"C:\Users\Marco\.gemini\antigravity\brain\42d0f7f9-bcc7-4184-a804-8c96eefd40aa\fluxo_jornada_referencia.png")

fig.savefig(out_project, format='png', dpi=300, bbox_inches='tight')
fig.savefig(out_brain, format='png', dpi=300, bbox_inches='tight')

print(f"Versão idêntica gerada com sucesso em:\n{out_project}\n{out_brain}")
