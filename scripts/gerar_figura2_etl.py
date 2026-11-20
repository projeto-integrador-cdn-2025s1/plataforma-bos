import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# 1. Título e subtítulo
ax.text(0.8, 8.35, "FIGURA 2 — FLUXO DO PIPELINE DE DADOS (ETL) DO PROJETO", 
        fontsize=16, fontweight='bold', color='#0f2d4a', va='center')
ax.text(0.8, 7.85, "ARQUITETURA DE INGESTÃO, TRATAMENTO E CONSUMO DOS DADOS — BANCO DE OLHOS DE SOROCABA", 
        fontsize=10.5, fontweight='bold', color='#52799c', va='center')

# Cores
c_border_gray = '#64748b'
c_etl_blue = '#0284c7'
c_etl_dark = '#0369a1'
c_card_bg = '#f8fafc'

# 2. COLUNA 1: FONTES DE DADOS
x1 = 0.8
w1 = 2.7
h_src = 1.35

ax.text(x1 + w1/2, 7.15, "1. FONTES DE DADOS", ha='center', va='center', fontsize=11, fontweight='bold', color='#1e293b')

sources = [
    ("Sistema MV Hospitalar", "Exportação tabular (CSV/XLSX)\nAtendimentos, agendas e cirurgias", 5.4),
    ("Registros Ambulatoriais", "Exames, procedimentos de catarata\ne médicos alocados (14k+ linhas)", 3.8),
    ("Base de Conhecimento BOS", "Perguntas frequentes, preparo,\norientações pré/pós e regulação SUS", 2.2)
]

for title, desc, y_pos in sources:
    box = patches.FancyBboxPatch((x1, y_pos), w1, h_src, boxstyle="round,pad=0.08,rounding_size=0.15",
                                 linewidth=1.6, edgecolor=c_border_gray, facecolor=c_card_bg)
    ax.add_patch(box)
    ax.text(x1 + w1/2, y_pos + h_src - 0.38, title, ha='center', va='center', fontsize=10, fontweight='bold', color='#0f172a')
    ax.text(x1 + w1/2, y_pos + 0.42, desc, ha='center', va='center', fontsize=8, color='#475569', linespacing=1.2)
    
    # Seta para o bloco de Extração [E]
    ax.annotate('', xy=(4.2, 5.75), xytext=(x1 + w1 + 0.05, y_pos + h_src/2),
                arrowprops=dict(arrowstyle="-|>", color="#94a3b8", lw=1.8, mutation_scale=14))

# 3. COLUNA 2: PIPELINE ETL EM PYTHON (Ordem correta: E -> T -> L)
x2 = 4.2
w2 = 3.6
h2 = 5.2
y2 = 1.95

box_etl = patches.FancyBboxPatch((x2, y2), w2, h2, boxstyle="round,pad=0.1,rounding_size=0.18",
                                linewidth=2.0, edgecolor=c_etl_blue, facecolor='#f8fafc')
ax.add_patch(box_etl)

header_box = patches.FancyBboxPatch((x2, y2 + h2 - 0.65), w2, 0.65, boxstyle="round,pad=0.05,rounding_size=0.15",
                                    linewidth=0, facecolor=c_etl_dark)
ax.add_patch(header_box)
ax.text(x2 + w2/2, y2 + h2 - 0.32, "2. PROCESSAMENTO ETL (PYTHON)", ha='center', va='center', fontsize=11, fontweight='bold', color='#FFFFFF')

# Fases do ETL organizadas de cima para baixo: Extração -> Transformação -> Carga
# Bloco E (Extração) no topo
box_e = patches.FancyBboxPatch((x2 + 0.2, 5.25), w2 - 0.4, 1.15, boxstyle="round,pad=0.06,rounding_size=0.12",
                               linewidth=1.3, edgecolor=c_etl_blue, facecolor='#FFFFFF')
ax.add_patch(box_e)
ax.text(x2 + 0.35, 6.15, "[E] EXTRAÇÃO (INGESTÃO)", ha='left', va='center', fontsize=9.5, fontweight='bold', color=c_etl_blue)
desc_e = "• Leitura de arquivos tabulares (CSV/XLSX)\n• Validação de schemas e diagnóstico inicial\n• Verificação de campos essenciais definidos"
ax.text(x2 + 0.35, 5.68, desc_e, ha='left', va='center', fontsize=7.8, color='#334155', linespacing=1.2)

# Seta E -> T (para baixo)
ax.annotate('', xy=(x2 + w2/2, 4.95), xytext=(x2 + w2/2, 5.23),
            arrowprops=dict(arrowstyle="-|>", color=c_etl_blue, lw=2.0, mutation_scale=14))

# Bloco T (Transformação) no meio
box_t = patches.FancyBboxPatch((x2 + 0.2, 3.4), w2 - 0.4, 1.5, boxstyle="round,pad=0.06,rounding_size=0.12",
                               linewidth=1.3, edgecolor=c_etl_dark, facecolor='#FFFFFF')
ax.add_patch(box_t)
ax.text(x2 + 0.35, 4.65, "[T] TRANSFORMAÇÃO & LIMPEZA", ha='left', va='center', fontsize=9.5, fontweight='bold', color=c_etl_dark)
desc_t = "• Remoção de duplicidades e inconsistências\n• Padronização de datas (YYYY-MM-DD / ISO)\n• Normalização de 48 municípios (DRS XVI)\n• Higienização de CPF, CNS e telefones\n• Conformidade com LGPD (dados protegidos)"
ax.text(x2 + 0.35, 4.0, desc_t, ha='left', va='center', fontsize=7.8, color='#334155', linespacing=1.2)

# Seta T -> L (para baixo)
ax.annotate('', xy=(x2 + w2/2, 3.1), xytext=(x2 + w2/2, 3.38),
            arrowprops=dict(arrowstyle="-|>", color=c_etl_blue, lw=2.0, mutation_scale=14))

# Bloco L (Carga) na base
box_l = patches.FancyBboxPatch((x2 + 0.2, 2.1), w2 - 0.4, 0.95, boxstyle="round,pad=0.06,rounding_size=0.12",
                               linewidth=1.3, edgecolor=c_etl_blue, facecolor='#FFFFFF')
ax.add_patch(box_l)
ax.text(x2 + 0.35, 2.82, "[L] CARGA (LOAD)", ha='left', va='center', fontsize=9.5, fontweight='bold', color=c_etl_blue)
desc_l = "• Mapeamento relacional de entidades\n• Inserção estruturada em lote (bulk insert)\n• Criação de índices para consultas rápidas"
ax.text(x2 + 0.35, 2.45, desc_l, ha='left', va='center', fontsize=7.8, color='#334155', linespacing=1.2)

# Seta do ETL (Carga) para a Base Relacional
ax.annotate('', xy=(8.5, 4.45), xytext=(x2 + w2 + 0.05, 3.0),
            arrowprops=dict(arrowstyle="-|>", color=c_etl_blue, lw=2.4, mutation_scale=18))

# 4. COLUNA 3: ARMAZENAMENTO RELACIONAL
x3 = 8.5
w3 = 3.0
h3 = 5.2
y3 = 1.95

box_db = patches.FancyBboxPatch((x3, y3), w3, h3, boxstyle="round,pad=0.1,rounding_size=0.18",
                                linewidth=2.0, edgecolor='#0369a1', facecolor='#e0f2fe')
ax.add_patch(box_db)

ax.text(x3 + w3/2, y3 + h3 - 0.45, "3. BASE RELACIONAL\nCENTRALIZADA", ha='center', va='center', fontsize=11, fontweight='bold', color='#0c4a6e', linespacing=1.2)
ax.text(x3 + w3/2, y3 + h3 - 0.95, "(Single Source of Truth)", ha='center', va='center', fontsize=8.5, color='#0369a1', style='italic')

# Tabelas limpas sem emojis incompatíveis
tables = [
    ("pacientes", "Identificação, nascimento, endereço e cidade"),
    ("profissionais", "Corpo clínico oftalmológico (120 médicos)"),
    ("solicitacoes_atendimento", "Protocolo BOS, prioridade (P1-P4), CID, status"),
    ("agendamentos", "Data agendada, confirmação e realização"),
    ("base_conhecimento", "FAQ homologado para orientação do paciente")
]

ytab = y3 + h3 - 1.45
for tname, tdesc in tables:
    tbox = patches.FancyBboxPatch((x3 + 0.2, ytab - 0.4), w3 - 0.4, 0.58, boxstyle="round,pad=0.04,rounding_size=0.08",
                                  linewidth=1.0, edgecolor='#7dd3fc', facecolor='#FFFFFF')
    ax.add_patch(tbox)
    ax.text(x3 + 0.35, ytab - 0.05, f"TABELA: {tname}", ha='left', va='center', fontsize=8.5, fontweight='bold', color='#0369a1')
    ax.text(x3 + 0.35, ytab - 0.25, tdesc, ha='left', va='center', fontsize=7.0, color='#64748b')
    ytab -= 0.68

# Setas do Banco para Consumo
ax.annotate('', xy=(12.3, 5.8), xytext=(x3 + w3 + 0.05, 5.1),
            arrowprops=dict(arrowstyle="-|>", color=c_etl_blue, lw=2.0, mutation_scale=16))
ax.annotate('', xy=(12.3, 3.1), xytext=(x3 + w3 + 0.05, 3.8),
            arrowprops=dict(arrowstyle="-|>", color=c_etl_blue, lw=2.0, mutation_scale=16))

# 5. COLUNA 4: CAMADA DE CONSUMO
x4 = 12.3
w4 = 2.9
h_dest = 2.1

ax.text(x4 + w4/2, 7.15, "4. CAMADA DE CONSUMO", ha='center', va='center', fontsize=11, fontweight='bold', color='#1e293b')

# Destino 1: Dashboard e BI
y_dest1 = 4.8
box_d1 = patches.FancyBboxPatch((x4, y_dest1), w4, h_dest, boxstyle="round,pad=0.08,rounding_size=0.15",
                                linewidth=1.8, edgecolor='#334155', facecolor='#f8fafc')
ax.add_patch(box_d1)
ax.text(x4 + w4/2, y_dest1 + h_dest - 0.4, "Dashboard de Gestão\n(Streamlit / Power BI)", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#0f172a', linespacing=1.2)
d1_desc = "• Monitoramento de filas SUS em tempo real\n• Alocação médica por cirurgião e dia\n• Distribuição regional (Sorocaba vs Fora)\n• Tempos de espera e prioridades (P1 a P4)"
ax.text(x4 + 0.2, y_dest1 + 0.65, d1_desc, ha='left', va='center', fontsize=7.8, color='#334155', linespacing=1.25)

# Destino 2: Chatbot e Consulta Pública
y_dest2 = 2.1
box_d2 = patches.FancyBboxPatch((x4, y_dest2), w4, h_dest, boxstyle="round,pad=0.08,rounding_size=0.15",
                                linewidth=1.8, edgecolor='#334155', facecolor='#f8fafc')
ax.add_patch(box_d2)
ax.text(x4 + w4/2, y_dest2 + h_dest - 0.4, "Chatbot & Consulta\n(Plataforma BOS Web)", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#0f172a', linespacing=1.2)
d2_desc = "• Consulta pública por protocolo ou CPF\n• Acompanhamento transparente do status\n• Assistente virtual 24/7 com FAQ validado\n• Orientações sobre exames e cirurgias"
ax.text(x4 + 0.2, y_dest2 + 0.65, d2_desc, ha='left', va='center', fontsize=7.8, color='#334155', linespacing=1.25)

# Linha de rodapé
ax.plot([0.8, 15.2], [0.85, 0.85], color='#cbd5e1', lw=1)
ax.text(0.8, 0.6, "Fonte: elaborado pelos autores (2026).", fontsize=9, color='#475569', style='italic', va='center')
ax.text(15.2, 0.6, "Projeto Piloto: Processo de Catarata — Banco de Olhos de Sorocaba", fontsize=9, color='#64748b', ha='right', va='center')

plt.subplots_adjust(left=0.03, right=0.97, top=0.95, bottom=0.05)

out_project = Path(r"C:\Users\Marco\Desktop\lo-files\computher showt\plataforma-bos\figura2_pipeline_etl.png")
out_brain = Path(r"C:\Users\Marco\.gemini\antigravity\brain\42d0f7f9-bcc7-4184-a804-8c96eefd40aa\figura2_pipeline_etl.png")

fig.savefig(out_project, format='png', dpi=300, bbox_inches='tight')
fig.savefig(out_brain, format='png', dpi=300, bbox_inches='tight')

print(f"Figura 2 regenerada com sucesso em:\n{out_project}\n{out_brain}")
