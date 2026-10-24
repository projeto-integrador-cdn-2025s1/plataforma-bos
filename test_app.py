import unittest
from app import iniciar
from app.extensions import db
from app.models import Paciente, SolicitacaoAtendimento

class TestPlataformaBOS(unittest.TestCase):
    def setUp(self):
        self.app = iniciar()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("Banco de Olhos de Sorocaba", html)
        self.assertIn("Consultar Atendimento", html)
        self.assertIn("/consulta", html)
        self.assertIn("/chat", html)
        self.assertIn("/duvidas", html)
        self.assertIn("/contatos", html)
        self.assertIn("/painel", html)

    def test_consulta_get(self):
        response = self.client.get('/consulta')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("Consulta de Atendimento SUS", html)
        self.assertIn("BOS-2026-001", html)

    def test_consulta_busca_protocolo_existente(self):
        response = self.client.get('/consulta?busca=BOS-2026-001')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("BOS-2026-001", html)
        self.assertIn("Consulta Agendada", html)
        self.assertIn("Dr. Ricardo Mendes", html)

    def test_consulta_busca_cpf(self):
        response = self.client.get('/consulta?busca=123.456.789-00')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("BOS-2026-001", html)

    def test_consulta_busca_inexistente(self):
        response = self.client.get('/consulta?busca=INVALIDO999')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("Nenhuma solicitação ou agendamento encontrado", html)

    def test_duvidas_page(self):
        response = self.client.get('/duvidas')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("Dúvidas Frequentes", html)

    def test_contatos_page(self):
        response = self.client.get('/contatos')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("Canais Oficiais de Atendimento", html)

    def test_chat_page(self):
        response = self.client.get('/chat')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("Assistente Virtual do BOS", html)

    def test_api_verificar_municipio_pertence(self):
        response = self.client.get('/api/verificar-municipio?cidade=Sorocaba')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['pertence'])

    def test_api_verificar_municipio_nao_pertence(self):
        response = self.client.get('/api/verificar-municipio?cidade=Campinas')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertFalse(data['pertence'])

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("Painel de Atendimento SUS", html)

    def test_painel_dashboard(self):
        response = self.client.get('/painel')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("PAINEL GERENCIAL SUS", html)
        self.assertIn("chartStatus", html)
        self.assertIn("chartEspecialidades", html)
        self.assertIn("chartRegiao", html)
        self.assertIn("chartCanais", html)
        self.assertIn("Gestão de Solicitações e Agendamentos", html)

    def test_atualizar_status_solicitacao(self):
        # Atualiza o status da solicitação 3 para AGENDADA
        response = self.client.post('/painel/atualizar-status', data={
            'solicitacao_id': 3,
            'novo_status': 'AGENDADA',
            'data_agendada': '2026-11-20T10:00',
            'profissional_id': 4
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            s = SolicitacaoAtendimento.query.get(3)
            self.assertEqual(s.status, 'AGENDADA')

if __name__ == '__main__':
    unittest.main()
