from flask import Blueprint, jsonify, request
from controllers.general_controllers import (
    get_index,
    get_chat,
    get_consulta,
    get_duvidas,
    get_contatos,
    verificar_municipio_api,
    get_painel,
    atualizar_status_solicitacao,
    login_funcionario,
    logout_funcionario
)
from app.model.chat import processar_duvida

rotas_gerais = Blueprint('rotas_gerais', __name__)

# --- ROTAS PÚBLICAS / PACIENTE ---

@rotas_gerais.route('/', methods=['GET', 'POST'])
def index():
    return get_index()

@rotas_gerais.route('/chat', methods=['GET', 'POST'])
def chat():
    # Rota e processamento do chat estritamente preservados
    if request.method == "POST":
        duvida = request.form.get('mensagem', "").strip()
        resposta = processar_duvida(str(duvida))
        return jsonify({
            "resposta": resposta
        })
            
    return get_chat()

@rotas_gerais.route('/consulta', methods=['GET', 'POST'])
def consulta():
    return get_consulta()

@rotas_gerais.route('/duvidas', methods=['GET'])
def duvidas():
    return get_duvidas()

@rotas_gerais.route('/contatos', methods=['GET'])
def contatos():
    return get_contatos()

@rotas_gerais.route('/api/verificar-municipio', methods=['GET'])
def api_verificar_municipio():
    return verificar_municipio_api()

# --- ROTAS GERENCIAIS / FUNCIONÁRIOS DO BOS ---

@rotas_gerais.route('/login', methods=['GET', 'POST'])
def login():
    return login_funcionario()

@rotas_gerais.route('/logout', methods=['GET'])
def logout():
    return logout_funcionario()

@rotas_gerais.route('/painel', methods=['GET'])
def painel():
    return get_painel()

@rotas_gerais.route('/painel/atualizar-status', methods=['POST'])
def atualizar_status():
    return atualizar_status_solicitacao()
