"""
Módulo de processamento do chatbot institucional do BOS.

Estratégia em camadas:
1. Gemini API (google-generativeai) — requer GEMINI_API_KEY no .env
2. Fallback local — busca por palavras-chave no base_info.txt (sem API, sem custo)
"""

import os
import re
import textwrap
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

diretorio_projeto = Path(__file__).resolve().parents[2]
load_dotenv(diretorio_projeto / ".env")

caminho_base = Path(__file__).resolve().parent / "base_info.txt"
informacao_base = caminho_base.read_text(encoding="utf-8")

# Pré-processa os parágrafos para o fallback local
_paragrafos = [p.strip() for p in re.split(r"\n{2,}", informacao_base) if p.strip()]

# ---------------------------------------------------------------------------
# Camada 1 — Gemini API
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = f"""Você é o assistente virtual do Banco de Olhos de Sorocaba (BOS), voltado ao atendimento de pacientes do SUS.
Responda em português brasileiro, com clareza, educação e linguagem acessível.
Utilize o contexto institucional abaixo para responder às perguntas dos usuários.
Não invente informações sobre consultas, contatos, prazos ou procedimentos.
Não forneça diagnósticos ou recomendações médicas individualizadas.
Se não souber responder, oriente o paciente a procurar os canais oficiais do BOS.

CONTEXTO INSTITUCIONAL:
{informacao_base}

FORMATAÇÃO DAS RESPOSTAS:
- Responda diretamente à pergunta do usuário.
- Utilize Markdown para organizar as respostas.
- Use **negrito** para destacar informações importantes, horários, documentos e contatos.
- Quando houver várias etapas ou documentos, utilize listas.
- Separe assuntos diferentes em parágrafos curtos.
- Evite respostas excessivamente longas e blocos de texto extensos.
- Não repita a apresentação inicial do assistente em cada resposta.
- Não invente informações que não estejam no contexto institucional.
"""


def _processar_com_gemini(duvida: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY não encontrada.")

    import google.generativeai as genai  # import tardio — só executa se a chave existir

    genai.configure(api_key=api_key)
    modelo = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=_SYSTEM_PROMPT,
    )
    resposta = modelo.generate_content(duvida)
    return resposta.text.strip()


# ---------------------------------------------------------------------------
# Camada 2 — Fallback local (busca por palavras-chave)
# ---------------------------------------------------------------------------

_RESPOSTAS_DIRETAS = {
    # Contatos / horários
    ("telefone", "contato", "ligar", "falar", "whatsapp", "email", "e-mail"): (
        "Você pode entrar em contato com o BOS pelos seguintes canais:\n\n"
        "- 📞 **Telefone:** (15) 3212-7000, opção **03**\n"
        "- ✉️ **E-mail:** sus@bos.org.br\n"
        "- 💬 **WhatsApp transplante:** (15) 3212-7891 ou (15) 3212-7040\n\n"
        "**Horário de atendimento:** segunda a sexta-feira, das **8h às 18h**.\n"
        "**Agendamento:** segunda a sexta-feira, das **7h às 16h**."
    ),
    # Primeira consulta
    ("primeira consulta", "agendar consulta", "marcar consulta", "primeira vez"): (
        "Para agendar uma **primeira consulta** pelo SUS:\n\n"
        "1. Procure a **UBS (Unidade Básica de Saúde)** mais próxima da sua casa.\n"
        "2. Peça o encaminhamento para o BOS.\n"
        "3. Aguarde o contato da **Central de Vagas** com a data e horário.\n\n"
        "No dia da consulta, leve: **Guia de Referência, RG, CPF, Cartão SUS e comprovante de residência**."
    ),
    # Retorno
    ("retorno", "agendar retorno", "marcar retorno", "consulta de retorno"): (
        "Para agendar um **retorno**:\n\n"
        "- Moradores de Sorocaba e região: compareça presencialmente, ligue ou envie e-mail para a Central de Atendimento SUS.\n"
        "- De fora da região: envie a solicitação médica digitalizada para **sus@bos.org.br** com nome completo, nome da mãe e data de nascimento.\n\n"
        "📞 (15) 3212-7000, opção 03 | ✉️ sus@bos.org.br"
    ),
    # TFD
    ("tfd", "tratamento fora", "declaração", "tfd"): (
        "A **Declaração de Tratamento Fora de Domicílio (TFD)** é fornecida a pacientes que:\n\n"
        "- Já possuem consulta agendada, e\n"
        "- Residem **fora** da região de Sorocaba.\n\n"
        "Solicite pelo telefone **(15) 3212-7000**, opção 03, ou pelo e-mail **sus@bos.org.br**.\n"
        "O documento é enviado por e-mail em até **24 horas**."
    ),
    # Transplante
    ("transplante", "córnea", "cornea"): (
        "Para avaliação de **transplante de córnea**:\n\n"
        "1. Obtenha um **laudo médico** com diagnóstico e indicação para transplante.\n"
        "2. Entre em contato pelo WhatsApp: **(15) 3212-7891** (para pacientes de fora da região) ou **(15) 3212-7040**.\n"
        "3. Siga as instruções e aguarde o chamado do hospital.\n\n"
        "✉️ transplante@bos.org.br"
    ),
    # Documentos
    ("documento", "laudo", "solicitar documento", "atestado"): (
        "Para solicitar documentos médicos:\n\n"
        "Acesse **https://bos.org.br/solicitar-documentos/** e siga as instruções disponíveis no site."
    ),
    # Horário de funcionamento
    ("horário", "horario", "funciona", "funcionamento", "aberto"): (
        "**Horários do BOS:**\n\n"
        "- Central de Atendimento SUS: **segunda a sexta, 8h às 18h**\n"
        "- Central de Agendamento SUS: **segunda a sexta, 7h às 16h**\n\n"
        "📞 (15) 3212-7000, opção 03 | ✉️ sus@bos.org.br"
    ),
    # Documentos para levar
    ("documentos", "levar", "preciso trazer", "o que trazer", "o que levar"): (
        "No dia do atendimento, leve:\n\n"
        "- 🪪 **RG** (original ou cópia)\n"
        "- 📋 **CPF**\n"
        "- 💳 **Cartão Nacional de Saúde (Cartão SUS)**\n"
        "- 🏠 **Comprovante de residência**\n"
        "- 📄 **Guia de Referência** (encaminhamento da UBS)\n"
        "- ☎️ **Telefone para contato**"
    ),
    # Municípios / cidades
    ("município", "municipio", "cidade", "região", "regiao", "minha cidade"): (
        "Os municípios da região de Sorocaba atendidos pelo BOS incluem: Sorocaba, Itu, Salto, Tatuí, "
        "Itapetininga, Votorantim, São Roque, Mairinque, Boituva, entre outros.\n\n"
        "Consulte a lista completa em **https://bos.org.br/atendimento-sus/#cidades** ou ligue para "
        "(15) 3212-7000, opção 03."
    ),
}


def _fallback_local(duvida: str) -> str:
    """Busca resposta por palavras-chave no dicionário de respostas diretas,
    com fallback para busca nos parágrafos do base_info.txt."""
    duvida_lower = duvida.lower()

    # 1. Tenta correspondência direta por palavras-chave
    melhor_score = 0
    melhor_resposta = None
    for chaves, resposta in _RESPOSTAS_DIRETAS.items():
        score = sum(1 for k in chaves if k in duvida_lower)
        if score > melhor_score:
            melhor_score = score
            melhor_resposta = resposta

    if melhor_score >= 1 and melhor_resposta:
        return melhor_resposta

    # 2. Busca por palavras nos parágrafos do base_info.txt
    palavras = set(re.findall(r"\w{4,}", duvida_lower))
    if palavras:
        scored = []
        for paragrafo in _paragrafos:
            p_lower = paragrafo.lower()
            hits = sum(1 for w in palavras if w in p_lower)
            if hits:
                scored.append((hits, paragrafo))
        scored.sort(key=lambda x: x[0], reverse=True)
        if scored:
            top = scored[0][1]
            # Limita o tamanho da resposta para ser legível
            if len(top) > 800:
                top = top[:800].rsplit(".", 1)[0] + "."
            return (
                top + "\n\n---\n*Para mais informações, entre em contato com a Central de Atendimento SUS: "
                "(15) 3212-7000, opção 03, de segunda a sexta-feira, das 8h às 18h, ou sus@bos.org.br.*"
            )

    # 3. Resposta padrão
    return (
        "Não encontrei uma resposta específica para sua dúvida.\n\n"
        "Por favor, entre em contato diretamente com o **Banco de Olhos de Sorocaba**:\n\n"
        "- 📞 **(15) 3212-7000**, opção 03 — segunda a sexta, **8h às 18h**\n"
        "- ✉️ **sus@bos.org.br**\n\n"
        "Nossa equipe terá o prazer em ajudá-lo!"
    )


# ---------------------------------------------------------------------------
# Função pública
# ---------------------------------------------------------------------------

def processar_duvida(duvida_usuario: str) -> str:
    """Processa a dúvida do usuário e retorna uma resposta em Markdown.

    Tenta a Gemini API primeiro; se não disponível, usa o fallback local.
    """
    duvida_usuario = str(duvida_usuario).strip()

    if not duvida_usuario:
        raise ValueError("A pergunta não pode estar vazia.")

    # Camada 1 — Gemini (se a chave estiver configurada)
    try:
        return _processar_com_gemini(duvida_usuario)
    except EnvironmentError:
        pass  # chave não configurada → usa fallback
    except Exception:
        pass  # erro de rede, cota, etc. → usa fallback

    # Camada 2 — Fallback local
    return _fallback_local(duvida_usuario)
