from datetime import date, datetime
from secrets import token_hex

from .extensions import db


# 1. PACIENTE
# Armazena os dados de identificação e contato.
# Um paciente pode ter várias solicitações de atendimento.

class Paciente(db.Model):
    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True)

    nome_completo = db.Column(db.String(150), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=True)
    nome_mae = db.Column(db.String(150), nullable=True)

    cpf = db.Column(db.String(11), unique=True, nullable=True)
    cns = db.Column(db.String(15), unique=True, nullable=True)

    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), nullable=True)

    # Endereço
    cep = db.Column(db.String(8), nullable=True)
    rua = db.Column(db.String(150), nullable=True)
    numero = db.Column(db.String(15), nullable=True)
    complemento = db.Column(db.String(100), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(2), nullable=True)

    data_cadastro = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )

    # Relacionamento: um paciente pode ter várias solicitações.
    solicitacoes = db.relationship(
        "SolicitacaoAtendimento",
        back_populates="paciente"
    )

    @property
    def idade(self):
        """Calcula a idade com base na data de nascimento."""
        if self.data_nascimento is None:
            return None

        hoje = date.today()

        return (
            hoje.year
            - self.data_nascimento.year
            - (
                (hoje.month, hoje.day)
                < (
                    self.data_nascimento.month,
                    self.data_nascimento.day
                )
            )
        )

    def __repr__(self):
        return f"<Paciente {self.id}: {self.nome_completo}>"

# 2. PROFISSIONAL
# Armazena os profissionais responsáveis pelos atendimentos.


class Profissional(db.Model):
    __tablename__ = "profissionais"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(150), nullable=False)
    especialidade = db.Column(db.String(120), nullable=False)

    ativo = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # Relacionamento: um profissional pode ter vários agendamentos.
    agendamentos = db.relationship(
        "Agendamento",
        back_populates="profissional"
    )

    def __repr__(self):
        return f"<Profissional {self.nome}>"



# 3. SOLICITACAO DE ATENDIMENTO
# Armazena os dados da solicitação e o acompanhamento na fila.

def gerar_protocolo():
    """Gera um identificador aleatório para acompanhamento."""
    return token_hex(10).upper()


class SolicitacaoAtendimento(db.Model):
    __tablename__ = "solicitacoes_atendimento"

    __table_args__ = (
        db.CheckConstraint(
            "prioridade IN ('P1', 'P2', 'P3', 'P4')",
            name="ck_solicitacao_prioridade"
        ),
        db.CheckConstraint(
            "status IN ("
            "'RECEBIDA', 'EM_TRIAGEM', 'AGUARDANDO', "
            "'AGENDADA', 'ENCERRADA', 'CANCELADA'"
            ")",
            name="ck_solicitacao_status"
        ),
        db.CheckConstraint(
            "canal_origem IN ("
            "'WHATSAPP', 'EMAIL', 'BALCAO', "
            "'TELEFONE', 'OUTRO'"
            ")",
            name="ck_solicitacao_canal"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    protocolo = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        default=gerar_protocolo
    )

    paciente_id = db.Column(
        db.Integer,
        db.ForeignKey("pacientes.id"),
        nullable=False
    )

    # Classificação da solicitação
    prioridade = db.Column(db.String(2), nullable=False)

    possui_pedido_medico = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    cid = db.Column(db.String(10), nullable=True)
    motivo_clinico = db.Column(db.Text, nullable=True)

    tipo_atendimento = db.Column(
        db.String(30),
        nullable=False
    )

    especialidade = db.Column(
        db.String(120),
        nullable=False
    )

    procedimento = db.Column(
        db.String(150),
        nullable=True
    )

    canal_origem = db.Column(
        db.String(20),
        nullable=False
    )

    # Situação da solicitação na fila
    status = db.Column(
        db.String(20),
        nullable=False,
        default="RECEBIDA"
    )

    data_solicitacao = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )

    data_atualizacao = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )

    data_encerramento = db.Column(
        db.DateTime,
        nullable=True
    )

    # Relacionamentos
    paciente = db.relationship(
        "Paciente",
        back_populates="solicitacoes"
    )

    agendamentos = db.relationship(
        "Agendamento",
        back_populates="solicitacao"
    )

    historico = db.relationship(
        "HistoricoSolicitacao",
        back_populates="solicitacao"
    )

    @property
    def tempo_espera_dias(self):
        """
        Calcula os dias entre a solicitação e:
        - a realização do primeiro atendimento;
        - o encerramento, se não houve atendimento realizado;
        - a data atual, se ainda estiver aberta.
        """

        datas_realizacao = [
            agendamento.data_realizacao.date()
            for agendamento in self.agendamentos
            if (
                agendamento.status == "REALIZADO"
                and agendamento.data_realizacao is not None
            )
        ]

        if datas_realizacao:
            data_final = min(datas_realizacao)

        elif self.data_encerramento is not None:
            data_final = self.data_encerramento.date()

        else:
            data_final = date.today()

        return max(
            (data_final - self.data_solicitacao.date()).days,
            0
        )

    def __repr__(self):
        return f"<Solicitacao {self.protocolo}>"


# 4. AGENDAMENTO
# Armazena a data marcada e os dados do atendimento.

class Agendamento(db.Model):
    __tablename__ = "agendamentos"

    __table_args__ = (
        db.CheckConstraint(
            "status IN ("
            "'AGENDADO', 'REALIZADO', 'CANCELADO', 'FALTOU'"
            ")",
            name="ck_agendamento_status"
        ),
        db.CheckConstraint(
            "status_confirmacao IN ("
            "'PENDENTE', 'CONFIRMADO', 'RECUSADO'"
            ")",
            name="ck_agendamento_confirmacao"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    solicitacao_id = db.Column(
        db.Integer,
        db.ForeignKey("solicitacoes_atendimento.id"),
        nullable=False
    )

    profissional_id = db.Column(
        db.Integer,
        db.ForeignKey("profissionais.id"),
        nullable=True
    )

    data_agendada = db.Column(
        db.DateTime,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="AGENDADO"
    )

    status_confirmacao = db.Column(
        db.String(20),
        nullable=False,
        default="PENDENTE"
    )

    data_realizacao = db.Column(
        db.DateTime,
        nullable=True
    )

    data_cadastro = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )

    data_atualizacao = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )

    # Relacionamentos
    solicitacao = db.relationship(
        "SolicitacaoAtendimento",
        back_populates="agendamentos"
    )

    profissional = db.relationship(
        "Profissional",
        back_populates="agendamentos"
    )

    def __repr__(self):
        return f"<Agendamento {self.id}: {self.status}>"

# 5. USUARIO
# Armazena as contas dos funcionários que acessam o painel.

class Usuario(db.Model):
    __tablename__ = "usuarios"

    __table_args__ = (
        db.CheckConstraint(
            "perfil IN ('ADMIN', 'ATENDIMENTO')",
            name="ck_usuario_perfil"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(150), nullable=False)

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    senha_hash = db.Column(
        db.String(255),
        nullable=False
    )

    perfil = db.Column(
        db.String(20),
        nullable=False,
        default="ATENDIMENTO"
    )

    ativo = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    data_cadastro = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )

    def __repr__(self):
        return f"<Usuario {self.email}>"

# 6. HISTORICO DA SOLICITACAO
# Registra as mudanças de status e quem as realizou.

class HistoricoSolicitacao(db.Model):
    __tablename__ = "historico_solicitacoes"

    id = db.Column(db.Integer, primary_key=True)

    solicitacao_id = db.Column(
        db.Integer,
        db.ForeignKey("solicitacoes_atendimento.id"),
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=True
    )

    status_anterior = db.Column(
        db.String(20),
        nullable=True
    )

    novo_status = db.Column(
        db.String(20),
        nullable=False
    )

    data_alteracao = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )

    # Relacionamentos
    solicitacao = db.relationship(
        "SolicitacaoAtendimento",
        back_populates="historico"
    )

    usuario = db.relationship("Usuario")

    def __repr__(self):
        return (
            f"<HistoricoSolicitacao "
            f"{self.id}: {self.novo_status}>"
        )

