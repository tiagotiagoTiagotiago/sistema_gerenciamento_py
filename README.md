
---

# Sistema de Gerenciamento de Empréstimo de Produtos

Este é um sistema simples de gerenciamento de empréstimo de produtos, construído com Flask e SQLAlchemy.

## Funcionalidades Principais

- **CRUD de Produtos:** Possibilidade de criar, listar, atualizar e excluir produtos do estoque.
- **CRUD de Funcionários:** Capacidade de adicionar, visualizar, atualizar e remover informações sobre os funcionários.
- **Empréstimo de Produtos:** Funcionalidade para permitir que os funcionários peguem produtos emprestados do estoque.

## Requisitos

- Python 3.x
- Flask
- SQLAlchemy
- Postgresql (ou outro banco de dados suportado pelo SQLAlchemy)

## Instalação

1. Clone este repositório em sua máquina local:

   ```bash
   https://github.com/tiagotiagoTiagotiago/sistema_gerenciamento_py.git
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd 
   ```

3. Instale as dependências usando pip:

   ```bash
   pip install Flask Flask-SQLAlchemy psycopg2-binary
   ```

4. Configure o banco de dados PostgreSQL:

   - Crie um banco de dados chamado `estoque_db`.
   - Altere a string de conexão do banco de dados em `app.py` conforme necessário.

5. Inicie o servidor Flask:

   ```bash
   python app.py
   ```

6. O servidor estará em execução em `http://localhost:5000`.


Criar um ambiente virtual:

python3 -m venv venv
Ativar o ambiente virtual (no Windows):
venv\Scripts\activate



