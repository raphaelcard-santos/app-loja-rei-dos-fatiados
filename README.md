# Aplicativo Rei dos Fatiados

Este é um aplicativo Flask desenvolvido para a loja "Rei dos Fatiados" para gerenciar clientes, compras, pagamentos e saldos devedores mensais.

## Funcionalidades

- Cadastro e gerenciamento de clientes.
- Registro de compras por cliente.
- Controle de pagamentos totais e parciais por compra.
- Cálculo de saldo devedor por compra.
- Fechamento mensal de compras: as compras de um mês específico são marcadas como encerradas e o saldo devedor total do cliente para aquele mês é transferido como uma nova "compra" (do tipo saldo devedor) para o mês subsequente.

## Estrutura do Projeto

```
rei_dos_fatiados_app/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cliente.py  # Modelo de dados para Clientes
│   │   └── compra.py   # Modelo de dados para Compras
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── cliente_routes.py  # Rotas para CRUD de Clientes
│   │   └── compra_routes.py   # Rotas para CRUD de Compras e fechamento mensal
│   ├── static/             # Arquivos estáticos (CSS, JS, imagens) - não utilizado neste backend API
│   └── main.py             # Ponto de entrada da aplicação Flask, configuração e criação do app
├── venv/                   # Ambiente virtual Python (não incluído no Git)
├── requirements.txt        # Dependências Python do projeto
└── .gitignore              # Arquivos e pastas a serem ignorados pelo Git
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

Certifique-se de criar o banco de dados (`mydb` ou o nome que você configurar) no seu servidor MySQL antes de rodar a aplicação pela primeira vez. As tabelas serão criadas automaticamente pela aplicação.

**Exemplo de como definir variáveis de ambiente (Linux/macOS):**
```bash
export DB_USERNAME="seu_usuario_mysql"
export DB_PASSWORD="sua_senha_mysql"
export DB_NAME="rei_dos_fatiados_db"
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

### Clientes

- `POST /clientes/`: Cria um novo cliente.
  - Corpo JSON: `{"nome": "Nome do Cliente", "telefone": "(XX) XXXXX-XXXX", "email": "cliente@exemplo.com"}`
- `GET /clientes/`: Lista todos os clientes.
- `GET /clientes/<int:cliente_id>`: Detalha um cliente específico.
- `PUT /clientes/<int:cliente_id>`: Atualiza um cliente existente.
  - Corpo JSON: (campos a serem atualizados)
- `DELETE /clientes/<int:cliente_id>`: Deleta um cliente.

### Compras

- `POST /compras/cliente/<int:cliente_id>`: Registra uma nova compra para um cliente.
  - Corpo JSON: `{"descricao": "Produto X", "valor_total": "100.50", "valor_pago": "50.00", "mes_referencia": 5, "ano_referencia": 2025}` (mês/ano são opcionais, padrão para data atual)
- `GET /compras/cliente/<int:cliente_id>`: Lista todas as compras de um cliente.
- `GET /compras/<int:compra_id>`: Detalha uma compra específica.
- `PUT /compras/<int:compra_id>`: Atualiza uma compra (descrição, valor_total, valor_pago).
  - Corpo JSON: (campos a serem atualizados)
- `DELETE /compras/<int:compra_id>`: Deleta uma compra (apenas se não houver pagamentos e não estiver encerrada).
- `POST /compras/<int:compra_id>/pagar`: Registra um pagamento para uma compra.
  - Corpo JSON: `{"valor_pagamento": "25.00"}`

### Fechamento Mensal

- `POST /compras/fechamento_mensal`: Realiza o fechamento das compras de um mês/ano específico para todos os clientes.
  - Corpo JSON: `{"mes": 5, "ano": 2025}`
  - Esta operação encerra as compras do período e transfere o saldo devedor para o mês seguinte como uma nova "compra" de saldo.

## Observações

- Este é um backend de API. Não há interface gráfica de usuário (frontend) incluída neste projeto. Você pode usar ferramentas como Postman, Insomnia ou curl para interagir com a API.
- A logo da loja não foi integrada, pois este é um serviço de backend. A logo seria utilizada em um frontend ou em relatórios gerados.
- O token do GitHub fornecido anteriormente (`Bekvi3-sexmez-bewqed`) era inválido. O repositório foi criado com o novo token fornecido (`ghp_Rp14...`).

## Próximos Passos Sugeridos

- Desenvolver uma interface de usuário (frontend web ou mobile) para interagir com esta API.
- Implementar autenticação e autorização para proteger os endpoints.
- Adicionar funcionalidades de relatório.
- Configurar um sistema de backup para o banco de dados.

