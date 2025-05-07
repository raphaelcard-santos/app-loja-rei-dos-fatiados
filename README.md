# Aplicativo Rei dos Fatiados

Este é um aplicativo Flask desenvolvido para a loja "Rei dos Fatiados" para gerenciar clientes, compras, pagamentos e saldos devedores mensais, com endpoints protegidos por autenticação JWT.

## Funcionalidades

- Cadastro e gerenciamento de clientes (protegido).
- Registro de compras por cliente (protegido).
- Controle de pagamentos totais e parciais por compra (protegido).
- Cálculo de saldo devedor por compra.
- Fechamento mensal de compras: as compras de um mês específico são marcadas como encerradas e o saldo devedor total do cliente para aquele mês é transferido como uma nova "compra" (do tipo saldo devedor) para o mês subsequente (protegido).
- Autenticação de usuários via JWT (JSON Web Tokens).

## Estrutura do Projeto

```
rei_dos_fatiados_app/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cliente.py      # Modelo de dados para Clientes
│   │   ├── compra.py       # Modelo de dados para Compras
│   │   └── usuario.py      # Modelo de dados para Usuários (autenticação)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py    # Rotas para autenticação (registro, login)
│   │   ├── cliente_routes.py # Rotas para CRUD de Clientes (protegidas)
│   │   └── compra_routes.py  # Rotas para CRUD de Compras e fechamento (protegidas)
│   ├── static/                 # Arquivos estáticos (não utilizado neste backend API)
│   └── main.py                 # Ponto de entrada da aplicação Flask, configuração e criação do app
├── venv/                       # Ambiente virtual Python (não incluído no Git)
├── requirements.txt            # Dependências Python do projeto
└── .gitignore                  # Arquivos e pastas a serem ignorados pelo Git
```

## Configuração e Execução

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Git
- Um servidor MySQL em execução.

### 1. Clonar o Repositório

```bash
git clone https://github.com/raphaelcard-santos/app-loja-rei-dos-fatiados.git
cd app-loja-rei-dos-fatiados
```

### 2. Configurar o Ambiente Virtual e Instalar Dependências

É altamente recomendável usar um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate    # No Windows

pip install -r requirements.txt
```

### 3. Configurar o Banco de Dados MySQL

O aplicativo espera que um servidor MySQL esteja rodando e acessível. As credenciais e o nome do banco de dados são configurados através de variáveis de ambiente ou diretamente no arquivo `src/main.py` (menos recomendado para produção).

As variáveis de ambiente esperadas são:
- `DB_USERNAME`: Nome de usuário do MySQL (padrão: `root`)
- `DB_PASSWORD`: Senha do MySQL (padrão: `password`)
- `DB_HOST`: Host do MySQL (padrão: `localhost`)
- `DB_PORT`: Porta do MySQL (padrão: `3306`)
- `DB_NAME`: Nome do banco de dados (padrão: `mydb`)
- `SECRET_KEY`: Chave secreta para Flask (ex: `os.urandom(24)`)
- `JWT_SECRET_KEY`: Chave secreta para JWT (ex: `super-secret-jwt`, **use um valor forte em produção**)

Certifique-se de criar o banco de dados (`mydb` ou o nome que você configurar) no seu servidor MySQL antes de rodar a aplicação pela primeira vez. As tabelas (incluindo `usuarios`) serão criadas automaticamente pela aplicação.

**Exemplo de como definir variáveis de ambiente (Linux/macOS):**
```bash
export DB_USERNAME="seu_usuario_mysql"
export DB_PASSWORD="sua_senha_mysql"
export DB_NAME="rei_dos_fatiados_db"
export SECRET_KEY="uma_chave_secreta_muito_forte"
export JWT_SECRET_KEY="outra_chave_secreta_ainda_mais_forte_para_jwt"
# etc.
```

### 4. Executar a Aplicação

Com o ambiente virtual ativado e as variáveis de ambiente configuradas (se necessário):

```bash
python src/main.py
```

A aplicação estará rodando em `http://0.0.0.0:5000/` por padrão.

## Endpoints da API

A aplicação expõe os seguintes endpoints:

### Autenticação (`/auth`)

- `POST /auth/register`: Registra um novo usuário.
  - Corpo JSON: `{"email": "usuario@exemplo.com", "senha": "senha123"}`
  - Resposta: Mensagem de sucesso e ID do usuário.
- `POST /auth/login`: Autentica um usuário e retorna um token JWT.
  - Corpo JSON: `{"email": "usuario@exemplo.com", "senha": "senha123"}`
  - Resposta: `{"access_token": "SEU_TOKEN_JWT"}`

**Para acessar os endpoints protegidos abaixo, você deve incluir o `access_token` no cabeçalho `Authorization` como um Bearer Token:**
`Authorization: Bearer SEU_TOKEN_JWT`

### Clientes (Protegido)

- `POST /clientes/`: Cria um novo cliente.
- `GET /clientes/`: Lista todos os clientes.
- `GET /clientes/<int:cliente_id>`: Detalha um cliente específico.
- `PUT /clientes/<int:cliente_id>`: Atualiza um cliente existente.
- `DELETE /clientes/<int:cliente_id>`: Deleta um cliente.

### Compras (Protegido)

- `POST /compras/cliente/<int:cliente_id>`: Registra uma nova compra para um cliente.
- `GET /compras/cliente/<int:cliente_id>`: Lista todas as compras de um cliente.
- `GET /compras/<int:compra_id>`: Detalha uma compra específica.
- `PUT /compras/<int:compra_id>`: Atualiza uma compra.
- `DELETE /compras/<int:compra_id>`: Deleta uma compra.
- `POST /compras/<int:compra_id>/pagar`: Registra um pagamento para uma compra.

### Fechamento Mensal (Protegido)

- `POST /compras/fechamento_mensal`: Realiza o fechamento das compras de um mês/ano específico.
  - Corpo JSON: `{"mes": 5, "ano": 2025}`

## Observações

- Este é um backend de API. Use ferramentas como Postman, Insomnia ou curl para interagir.
- A interface web (frontend) desenvolvida separadamente (`rei-dos-fatiados-frontend`) precisará ser atualizada para lidar com o fluxo de autenticação (login e envio do token JWT).
- A logo da loja não foi integrada, pois este é um serviço de backend. A logo seria utilizada em um frontend ou em relatórios gerados.

## Próximos Passos Sugeridos

- Integrar o fluxo de autenticação no frontend.
- Adicionar funcionalidades de relatório.
- Configurar um sistema de backup para o banco de dados.

