# DRE CRUD --- Registration System

### *FastAPI · PostgreSQL · Streamlit · Docker Compose*

## How to Run the Project

### 1. Clone the repository

    git clone https://github.com/alamounier/DRE_CRUD
    cd DRE_CRUD

### 2. Create environment variables

Inside the `backend/` folder, create a `.env` file:

    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_DB=mydatabase
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    API_URL=http://backend:8000

### 3. Start the application with Docker Compose

    docker-compose build
    docker-compose up -d

Backend: `http://localhost:8000`\
Frontend: `http://localhost:8501`

------------------------------------------------------------------------

## Project Structure

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
    │   └── requirements.txt
    │
    │── docker-compose.yml
    │── README.md

------------------------------------------------------------------------

## Technologies Used

### Backend

-   Python 3.9+
-   FastAPI
-   SQLAlchemy ORM
-   Pydantic
-   PostgreSQL
-   Psycopg2
-   Docker & Docker Compose

### Frontend

-   Streamlit
-   Requests

------------------------------------------------------------------------

## Available Endpoints (FastAPI)

### Stores

-   GET /stores/
-   POST /stores/
-   PUT /stores/{store_id}
-   DELETE /stores/{store_id}

### Employees

-   GET /employees/
-   POST /employees/
-   PUT /employees/{employee_id}
-   DELETE /employees/{employee_id}

### Products

-   GET /products/
-   POST /products/
-   PUT /products/{product_id}
-   DELETE /products/{product_id}

### Purchases

-   GET /purchases/
-   POST /purchases/
-   PUT /purchases/{purchase_id}
-   DELETE /purchases/{purchase_id}

------------------------------------------------------------------------

## API Documentation

-   Swagger UI: http://localhost:8000/docs
-   Redoc: http://localhost:8000/redoc

------------------------------------------------------------------------

## Database

Tables created automatically:

-   stores
-   employees
-   products
-   purchases

------------------------------------------------------------------------

## Frontend (Streamlit)

Features:

✔️ Register stores\
✔️ Register employees\
✔️ Register products\
✔️ Register purchases\
✔️ Dynamic listing via API

------------------------------------------------------------------------

## How the Application Was Structured

-   Separation of backend, frontend, and DB into containers\
-   Modularized CRUD, schemas, models, and routing\
-   REST architecture\
-   Streamlit UI communicating with FastAPI\
-   Full orchestration via Docker Compose

------------------------------------------------------------------------

## 📄 License

This project is free for personal or academic use.
