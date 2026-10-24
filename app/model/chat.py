import os
from pathlib import Path

from dotenv import load_dotenv
from ollama import Client


# Localiza a raiz do projeto
diretorio_projeto = Path(__file__).resolve().parents[2]

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(diretorio_projeto / ".env")


# Carrega o contexto institucional do BOS
caminho_base = Path(__file__).resolve().parent / "base_info.txt"
informacao_base = caminho_base.read_text(encoding="utf-8")


def configurar_agente():
    api_key = os.getenv("OLLAMA_API_KEY")

    if not api_key:
        raise ValueError(
            "A variável OLLAMA_API_KEY não foi encontrada no arquivo .env."
        )

    agente = Client(
        host="https://ollama.com",
        headers={
            "Authorization": f"Bearer {api_key}"
        }
    )

    return agente


def processar_duvida(duvida_usuario):
    duvida_usuario = str(duvida_usuario).strip()

    if not duvida_usuario:
        raise ValueError("A pergunta não pode estar vazia.")

    agente_chat = configurar_agente()

    resposta_modelo = agente_chat.chat(
        model="gemma4:31b",
        messages=[
            {
                "role": "system",
                "content": f"""Você é o assistente virtual do Banco de Olhos de Sorocaba (BOS), voltado ao atendimento de pacientes do SUS.
                Responda em português brasileiro, com clareza, educação e linguagem acessível.
                Utilize o contexto institucional abaixo para responder às perguntas dos usuários. Não invente informações sobre consultas, contatos, prazos ou procedimentos. Não forneça diagnósticos ou recomendações médicas individualizadas.
                Se não souber responder, oriente o paciente a procurar os canais oficiais do BOS.
                CONTEXTO INSTITUCIONAL: {informacao_base}
                
                FORMATAÇÃO DAS RESPOSTAS:
                - Responda diretamente à pergunta do usuário.
                - Utilize Markdown para organizar as respostas.
                - Use **negrito** para destacar informações importantes,
                horários, documentos e contatos.
                - Quando houver várias etapas ou documentos, utilize listas.
                - Separe assuntos diferentes em parágrafos curtos.
                - Evite respostas excessivamente longas e blocos de texto extensos.
                - Não apresente todas as possibilidades se uma única resposta
                for suficiente para resolver a dúvida.
                - Se precisar saber se o paciente reside em Sorocaba e região
                para orientar corretamente, faça essa pergunta antes de explicar
                os procedimentos específicos.
                - Não repita a apresentação inicial do assistente em cada resposta.
                - Não invente informações que não estejam no contexto institucional.
                """
            },
            {
                "role": "user",
                "content": duvida_usuario
            }
        ],
        stream=False
    )

    return resposta_modelo.message.content.strip()