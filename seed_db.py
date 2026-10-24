"""
Script de povoamento (seed) para o banco de dados do Banco de Olhos de Sorocaba (BOS).
Popula pacientes, profissionais, solicitações, agendamentos e usuários para o Dashboard Gerencial.
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "instance" / "bos.db"

def popular_banco():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # Cria tabelas caso ainda não existam
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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    # Limpa dados existentes para reinserir semente limpa
    cur.execute("DELETE FROM historico_solicitacoes")
    cur.execute("DELETE FROM agendamentos")
    cur.execute("DELETE FROM solicitacoes_atendimento")
    cur.execute("DELETE FROM profissionais")
    cur.execute("DELETE FROM pacientes")
    cur.execute("DELETE FROM usuarios")

    agora = datetime.now()

    # 1. Usuários para Acesso dos Funcionários
    usuarios = [
        (1, "Coordenação de Atendimento SUS", "atendimento@bos.org.br", "bos123", "ATENDIMENTO", 1, agora.strftime("%Y-%m-%d %H:%M:%S")),
        (2, "Gestor Geral BOS", "admin@bos.org.br", "admin123", "ADMIN", 1, agora.strftime("%Y-%m-%d %H:%M:%S"))
    ]
    cur.executemany("INSERT INTO usuarios (id, nome, email, senha_hash, perfil, ativo, data_cadastro) VALUES (?, ?, ?, ?, ?, ?, ?)", usuarios)

    # 2. Profissionais
    profissionais = [
        (1, "Dr. Ricardo Mendes", "Oftalmologia Geral", 1),
        (2, "Dra. Camila Fonseca", "Córnea e Doenças Externas", 1),
        (3, "Dr. Fernando Silveira", "Retina e Vítreo", 1),
        (4, "Dra. Juliana Alencar", "Otorrinolaringologia", 1)
    ]
    cur.executemany("INSERT INTO profissionais (id, nome, especialidade, ativo) VALUES (?, ?, ?, ?)", profissionais)

    # 3. Pacientes (10 pacientes distribuídos)
    pacientes = [
        (1, "Maria Aparecida Santos", "1978-05-14", "Neusa Santos", "12345678900", "700123456789012", "(15) 99876-5432", "maria.santos@email.com", "18010000", "Rua das Flores", "120", "Apto 3", "Centro", "Sorocaba", "SP", (agora - timedelta(days=20)).strftime("%Y-%m-%d %H:%M:%S")),
        (2, "João Carlos de Oliveira", "1965-11-23", "Rosa Maria", "23456789011", "700234567890123", "(15) 98123-4567", "joao.carlos@email.com", "18110000", "Av. São João", "450", "", "Vossoroca", "Votorantim", "SP", (agora - timedelta(days=12)).strftime("%Y-%m-%d %H:%M:%S")),
        (3, "Ana Paula Rodrigues", "1992-03-30", "Carmen Rodrigues", "34567890122", "700345678901234", "(11) 97654-3210", "ana.rodrigues@email.com", "13300000", "Rua Floriano Peixoto", "89", "", "Centro", "Itu", "SP", (agora - timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S")),
        (4, "Carlos Eduardo Silveira", "1983-08-19", "Helena Silveira", "45678901233", "700456789012345", "(19) 98765-1122", "carlos.silveira@email.com", "13010000", "Av. Francisco Glicério", "1020", "Sala 4", "Cambuí", "Campinas", "SP", (agora - timedelta(days=40)).strftime("%Y-%m-%d %H:%M:%S")),
        (5, "Beatriz Helena Monteiro", "1954-02-10", "Geni Monteiro", "56789012344", "700567890123456", "(15) 99112-3344", "beatriz.monteiro@email.com", "18040000", "Rua Santa Clara", "300", "", "Campolim", "Sorocaba", "SP", (agora - timedelta(days=18)).strftime("%Y-%m-%d %H:%M:%S")),
        (6, "Marcos Vinicius Pereira", "1989-12-05", "Sonia Pereira", "67890123455", "700678901234567", "(15) 99778-9900", "marcos.pereira@email.com", "18520000", "Rua José Bonifácio", "55", "", "Centro", "Cerquilho", "SP", (agora - timedelta(days=9)).strftime("%Y-%m-%d %H:%M:%S")),
        (7, "Lucia Helena Costa", "1960-07-22", "Alzira Costa", "78901234566", "700789012345678", "(15) 98822-1133", "lucia.costa@email.com", "18270000", "Rua XI de Agosto", "780", "", "Vila Dr. Laurindo", "Tatuí", "SP", (agora - timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")),
        (8, "Pedro Henrique Alves", "2001-09-15", "Silvia Alves", "89012345677", "700890123456789", "(11) 98455-6677", "pedro.alves@email.com", "13320000", "Av. Dom Pedro II", "110", "", "Centro", "Salto", "SP", (agora - timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S")),
        (9, "Tereza Cristina Faria", "1972-04-18", "Maria Luiza", "90123456788", "700901234567890", "(14) 99123-8899", "tereza.faria@email.com", "18400000", "Rua Coronel Levino", "42", "", "Centro", "Itapeva", "SP", (agora - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")),
        (10, "Gabriel Souza Martins", "1995-10-08", "Vera Lúcia", "01234567899", "700012345678901", "(11) 97111-2233", "gabriel.martins@email.com", "01310000", "Av. Paulista", "1500", "Apto 82", "Bela Vista", "São Paulo", "SP", (agora - timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S"))
    ]
    cur.executemany("""
    INSERT INTO pacientes (id, nome_completo, data_nascimento, nome_mae, cpf, cns, telefone, email, cep, rua, numero, complemento, bairro, cidade, estado, data_cadastro)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, pacientes)

    # 4. Solicitações de Atendimento (diversos status e especialidades)
    solicitacoes = [
        (1, "BOS-2026-001", 1, "P2", 1, "H52.1", "Miopia progressiva e baixa acuidade visual", "Primeira Consulta", "Oftalmologia Geral", "Consulta Oftalmológica e Refração Completa", "BALCAO", "AGENDADA", (agora - timedelta(days=20)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"), None),
        (2, "BOS-2026-002", 2, "P1", 1, "H18.6", "Ceratocone avançado em olho direito - indicação de transplante", "Avaliação Córnea", "Córnea e Doenças Externas", "Avaliação Pré-Transplante de Córnea e Topografia", "WHATSAPP", "EM_TRIAGEM", (agora - timedelta(days=12)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), None),
        (3, "BOS-2026-003", 3, "P3", 1, "H90.3", "Perda auditiva neurossensorial bilateral moderada", "Exame / Avaliação", "Otorrinolaringologia", "Audiometria Tonal e Vocal", "BALCAO", "AGUARDANDO", (agora - timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S"), None),
        (4, "BOS-2026-004", 4, "P2", 1, "H18.1", "Retorno para reavaliação corneana após procedimento", "Retorno SUS", "Córnea e Doenças Externas", "Reavaliação Oftalmológica Especializada", "EMAIL", "ENCERRADA", (agora - timedelta(days=40)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")),
        (5, "BOS-2026-005", 5, "P2", 1, "H35.3", "Degeneração macular relacionada à idade (DMRI) exsudativa", "Consulta Especializada", "Retina e Vítreo", "Mapeamento de Retina e OCT", "BALCAO", "AGENDADA", (agora - timedelta(days=18)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"), None),
        (6, "BOS-2026-006", 6, "P3", 1, "H40.1", "Suspeita de glaucoma primário de ângulo aberto", "Primeira Consulta", "Oftalmologia Geral", "Tonometria e Campimetria Computadorizada", "OUTRO", "EM_TRIAGEM", (agora - timedelta(days=9)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S"), None),
        (7, "BOS-2026-007", 7, "P2", 1, "H25.0", "Catarata senil bilateral com indicação cirúrgica", "Avaliação Cirúrgica", "Oftalmologia Geral", "Biometria Ocular e Avaliação Pré-Operatória", "TELEFONE", "AGENDADA", (agora - timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), None),
        (8, "BOS-2026-008", 8, "P4", 0, "H52.2", "Astigmatismo e cefaleia aos esforços visuais", "Primeira Consulta", "Oftalmologia Geral", "Exame Refratométrico", "BALCAO", "RECEBIDA", (agora - timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S"), None),
        (9, "BOS-2026-009", 9, "P3", 1, "H65.2", "Otite média serosa crônica com hipoacusia", "Primeira Consulta", "Otorrinolaringologia", "Otoscopia e Imitanciometria", "OUTRO", "RECEBIDA", (agora - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"), None),
        (10, "BOS-2026-010", 10, "P1", 1, "H18.5", "Distrofia corneana endotelial de Fuchs grave", "Avaliação Transplante", "Córnea e Doenças Externas", "Avaliação para Transplante Endotelial (DMEK)", "WHATSAPP", "EM_TRIAGEM", (agora - timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), None)
    ]
    cur.executemany("""
    INSERT INTO solicitacoes_atendimento (
        id, protocolo, paciente_id, prioridade, possui_pedido_medico, cid, motivo_clinico,
        tipo_atendimento, especialidade, procedimento, canal_origem, status,
        data_solicitacao, data_atualizacao, data_encerramento
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, solicitacoes)

    # 5. Agendamentos
    agendamentos = [
        (1, 1, 1, (agora + timedelta(days=15, hours=3)).strftime("%Y-%m-%d 09:30:00"), "AGENDADO", "CONFIRMADO", None, (agora - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")),
        (2, 4, 2, (agora - timedelta(days=5, hours=2)).strftime("%Y-%m-%d 14:00:00"), "REALIZADO", "CONFIRMADO", (agora - timedelta(days=5, hours=1)).strftime("%Y-%m-%d 14:45:00"), (agora - timedelta(days=35)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=5)).strftime("%Y-%m-%d 15:00:00")),
        (3, 5, 3, (agora + timedelta(days=18, hours=4)).strftime("%Y-%m-%d 10:15:00"), "AGENDADO", "PENDENTE", None, (agora - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")),
        (4, 7, 1, (agora + timedelta(days=22, hours=2)).strftime("%Y-%m-%d 11:00:00"), "AGENDADO", "CONFIRMADO", None, (agora - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"), (agora - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))
    ]
    cur.executemany("""
    INSERT INTO agendamentos (
        id, solicitacao_id, profissional_id, data_agendada, status, status_confirmacao,
        data_realizacao, data_cadastro, data_atualizacao
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, agendamentos)

    # 6. Histórico das Solicitações
    historico = [
        (1, 1, 1, None, "RECEBIDA", (agora - timedelta(days=20)).strftime("%Y-%m-%d 10:00:00")),
        (2, 1, 1, "RECEBIDA", "EM_TRIAGEM", (agora - timedelta(days=15)).strftime("%Y-%m-%d 14:00:00")),
        (3, 1, 1, "EM_TRIAGEM", "AGENDADA", (agora - timedelta(days=5)).strftime("%Y-%m-%d 11:30:00")),
        (4, 2, 1, None, "RECEBIDA", (agora - timedelta(days=12)).strftime("%Y-%m-%d 08:30:00")),
        (5, 2, 1, "RECEBIDA", "EM_TRIAGEM", (agora - timedelta(days=8)).strftime("%Y-%m-%d 09:00:00")),
        (6, 3, 1, None, "RECEBIDA", (agora - timedelta(days=6)).strftime("%Y-%m-%d 11:15:00")),
        (7, 3, 1, "RECEBIDA", "AGUARDANDO", (agora - timedelta(days=6)).strftime("%Y-%m-%d 16:00:00")),
        (8, 4, 1, "AGENDADA", "ENCERRADA", (agora - timedelta(days=5)).strftime("%Y-%m-%d 15:00:00")),
        (9, 5, 2, "EM_TRIAGEM", "AGENDADA", (agora - timedelta(days=3)).strftime("%Y-%m-%d 10:00:00")),
        (10, 7, 2, "EM_TRIAGEM", "AGENDADA", (agora - timedelta(days=1)).strftime("%Y-%m-%d 14:00:00"))
    ]
    cur.executemany("""
    INSERT INTO historico_solicitacoes (
        id, solicitacao_id, usuario_id, status_anterior, novo_status, data_alteracao
    ) VALUES (?, ?, ?, ?, ?, ?)
    """, historico)

    con.commit()
    con.close()
    print("Banco de dados do BOS populado com sucesso com dados ricos de teste e usuários gerenciais!")

if __name__ == "__main__":
    popular_banco()
