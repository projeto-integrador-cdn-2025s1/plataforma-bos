# Plataforma BOS - Banco de Olhos de Sorocaba

Sistema de gestão de atendimentos oftalmológicos para o Banco de Olhos de Sorocaba (BOS), desenvolvido com Flask e SQLAlchemy.

## Funcionalidades

### Área do Paciente (Pública)
- **Página Inicial** - Informações sobre o BOS e municípios atendidos
- **Chat** - Assistente virtual para dúvidas frequentes
- **Consulta de Protocolo** - Acompanhamento de solicitações por protocolo, CPF ou CNS
- **Dúvidas Frequentes** - Base de conhecimento sobre atendimentos
- **Contatos** - Informações de contato e verificação de município

### Área Gerencial (Restrita a Funcionários)
- **Painel de Controle** - Dashboard com métricas em tempo real
- **Gestão de Fila** - Visualização e atualização de status de solicitações
- **Agendamentos** - Criação e gerenciamento de agendamentos com profissionais
- **Relatórios** - Gráficos por status, especialidade, região, canal e prioridade

## Tecnologias

- **Backend**: Flask 3.1+, SQLAlchemy 2.0+
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Gráficos**: Chart.js

## Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd plataforma-bos

# Crie ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instale dependências
pip install -r requirements.txt

# Popule o banco com dados fictícios
python seed_db.py

# Execute a aplicação
python main.py
```

Acesse: http://localhost:5000

## Acesso ao Painel Gerencial

Após iniciar a aplicação, acesse `/login` com:
- **Admin**: admin@bos.org.br / admin123
- **Atendimento**: atendimento@bos.org.br / bos123

## Estrutura do Projeto

```
plataforma-bos/
├── app/
│   ├── __init__.py          # Factory da aplicação Flask
│   ├── models.py            # Modelos SQLAlchemy
│   ├── extensions.py        # Extensões (db)
│   ├── templates/           # Templates Jinja2
│   └── static/              # CSS, JS, imagens
├── controllers/
│   └── general_controllers.py  # Lógica das rotas
├── routes/
│   └── general.py           # Definição das rotas
├── data/                    # Arquivos de dados (CSV)
├── scripts/                 # Scripts auxiliares
├── docs/                    # Documentação e diagramas
├── instance/                # Banco de dados SQLite (gitignored)
├── main.py                  # Entry point
├── seed_db.py               # Povoamento do banco (dados fictícios)
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Dados Fictícios

Este repositório **não contém dados reais de pacientes**. O script `seed_db.py` gera:
- 5.000 pacientes fictícios com nomes, CPFs, CNS, endereços válidos
- 10 profissionais oftalmólogos fictícios
- 15.000 solicitações de atendimento com distribuição realista
- 7.550 agendamentos
- Histórico completo de alterações de status

Todos os dados são sintéticos e seguem as mesmas regras de negócio do sistema real.

## Licença

Este projeto está licenciado sob a **OpenBSD 3-Clause License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

**Desenvolvido para o Banco de Olhos de Sorocaba (BOS)**