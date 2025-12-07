# DRE CRUD - Sistema Cadastro
### FastAPI + PostgreSQL + Streamlit + Docker-Compose

Este projeto é um sistema completo de cadastro (CRUD) composto por:

-   **Backend** em **FastAPI**
-   **Banco de dados PostgreSQL**
-   **ORM SQLAlchemy**
-   **Frontend em Streamlit**
-   **Execução via Docker**

Ele permite gerenciar:

✔️ Lojas\
✔️ Funcionários\
✔️ Produtos\
✔️ Compras

------------------------------------------------------------------------

## Estrutura do Projeto

    DRE_CRUD/
    │── backend/
    │   ├── crud.py
    │   ├── database.py
    │   ├── main.py
    │   ├── models.py
    │   ├── router.py
    │   ├── schemas.py
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    │── frontend/
    │   ├── app.py
    │   └── requirements.txt (opcional)
    │
    │── docker-compose.yml (se você criar futuramente)
    │── README.md

------------------------------------------------------------------------

## Tecnologias Utilizadas

### **Backend**

-   Python 3.9+
-   FastAPI
-   SQLAlchemy ORM
-   Pydantic
-   PostgreSQL
-   Psycopg2
-   Docker + Docker Compose

### **Frontend**

-   Streamlit
-   Requests

------------------------------------------------------------------------

## Como executar o projeto

### 1. Configurar variáveis de ambiente

Crie um arquivo `.env` dentro de `backend/`:

    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_DB=mydatabase
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    API_URL=http://backend:8000

------------------------------------------------------------------------

## Rodando com Docker-Compose

Para iniciar todo o ambiente (Backend e Frontend), execute:

- docker-compose build (na primeira vez ou quando alterar o Dockerfile)
- docker-compose up -d (sobe todos os serviços em modo detached)

Após isso, o serviço de Backend estará disponível em:

- http://localhost:8080

E o serviço de Frontend em:

- http://localhost:8501/

------------------------------------------------------------------------

## Endpoints disponíveis (FastAPI)

A API expõe os seguintes recursos:

### **Stores**

-   `GET /stores/`
-   `POST /stores/`
-   `PUT /stores/{store_id}`
-   `DELETE /stores/{store_id}`

### **Employees**

-   `GET /employees/`
-   `POST /employees/`
-   `PUT /employees/{employee_id}`
-   `DELETE /employees/{employee_id}`

### **Products**

-   `GET /products/`
-   `POST /products/`
-   `PUT /products/{product_id}`
-   `DELETE /products/{product_id}`

### **Purchases**

-   `GET /purchases/`
-   `POST /purchases/`
-   `PUT /purchases/{purchase_id}`
-   `DELETE /purchases/{purchase_id}`

------------------------------------------------------------------------

## Documentação automática da API

Acesse:

**Swagger UI**

    http://localhost:8000/docs

**Redoc**

    http://localhost:8000/redoc

------------------------------------------------------------------------

## Banco de Dados

Ao iniciar o backend, as tabelas são criadas automaticamente pelo
SQLAlchemy:

-   `stores`
-   `employees`
-   `products`
-   `purchases`

Cada CRUD está organizado em:

-   `models.py`: Modelos SQLAlchemy\
-   `schemas.py`: Schemas Pydantic\
-   `crud.py`: Funções CRUD\
-   `router.py`: Rotas FastAPI

------------------------------------------------------------------------

## Frontend (Streamlit)

A interface permite:

✔️ Cadastrar lojas\
✔️ Cadastrar funcionários ligados a lojas\
✔️ Cadastrar produtos\
✔️ Cadastrar compras\
✔️ Listar opções dinâmicas consultando a API

------------------------------------------------------------------------

## Melhorias futuras

-   Criar página de listagem e edição no Streamlit\
-   Adicionar autenticação JWT\
-   Criar testes automatizados (pytest)\
-   Adicionar logging e tratativas de erro

------------------------------------------------------------------------

## Licença

Este projeto é livre para uso pessoal ou acadêmico.
