import streamlit as st
import os
import requests

location_names = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas", "BA": "Bahia",
    "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás",
    "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais",
    "PA": "Pará", "PB": "Paraíba", "PR": "Paraná", "PE": "Pernambuco", "PI": "Piauí",
    "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul",
    "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina", "SP": "São Paulo", 
    "SE": "Sergipe", "TO": "Tocantins"
}

API_URL = os.getenv("API_URL", "http://backend:8000")

st.title("Cadastro de Lojas, Produtos, Funcionários e Compras")

# ============================
# CADASTRAR LOJA
# ============================

st.header("Cadastrar Loja")
with st.form("store_form"):
    name = st.text_input("Store's Name")
    city = st.text_input("City")
    store_location = st.selectbox(
        "Selecione o Estado",
        list(location_names.keys()),
        format_func=lambda x: location_names[x]
    )
    store_code = st.text_input("Store Code")
    square_meter = st.text_input("Square Meter")
    submit_store = st.form_submit_button("Cadastrar")

    if submit_store:
        try:
            payload = {
                "name": name,
                "city": city,
                "state": store_location,
                "store_code": store_code,
                "square_meter": float(square_meter)
            }
            response = requests.post(f"{API_URL}/stores/", json=payload)

            if response.ok:
                st.success("Loja cadastrada!")
            else:
                st.error(f"Erro: {response.text}")
        except Exception as e:
            st.error(f"Erro: {e}")


# ============================
# LISTAR LOJAS
# ============================

try:
    stores = requests.get(f"{API_URL}/stores/").json()
    store_names = {store["name"]: store["id"] for store in stores}
except:
    stores = []
    store_names = {}

# ============================
# CADASTRAR FUNCIONÁRIO
# ============================

st.header("Cadastrar Funcionário")
with st.form("employee_form"):
    if store_names:
        selected_store = st.selectbox("Selecione a Loja", list(store_names.keys()))
    else:
        st.warning("Nenhuma loja cadastrada ainda.")
        selected_store = None

    employee_name = st.text_input("Funcionário")
    employee_salary = st.number_input("Salário", min_value=0.0)
    submit_employee = st.form_submit_button("Cadastrar Funcionário")

    if submit_employee:
        if not selected_store:
            st.error("Cadastre uma loja primeiro!")
        else:
            payload = {
                "store_id": store_names[selected_store],
                "name": employee_name,
                "salary": employee_salary
            }
            response = requests.post(f"{API_URL}/employees/", json=payload)

            if response.ok:
                st.success("Funcionário cadastrado!")
            else:
                st.error(f"Erro: {response.text}")


# ============================
# CADASTRAR PRODUTO
# ============================

product_catalog = {
    "Alimentos": ["Arroz 5kg", "Feijão Preto 1kg", "Macarrão Espaguete", "Açúcar 1kg"],
    "Bebidas": ["Refrigerante 2L", "Água Mineral", "Suco de Laranja"],
    "Higiene": ["Sabonete", "Shampoo", "Pasta de Dente"],
    "Limpeza": ["Detergente", "Amaciante", "Sabão em Pó"],
    "Eletrodomésticos": ["Liquidificador", "Air Fryer", "Micro-ondas"],
}

st.header("Cadastrar Produto")

with st.form("product_form"):
    category = st.selectbox("Categoria", list(product_catalog.keys()))
    name = st.selectbox("Produto", product_catalog[category])
    price = st.number_input("Preço (opcional)", min_value=0.00, step=0.10)
    submit_product = st.form_submit_button("Salvar Produto")

    if submit_product:
        payload = {
            "category": category,
            "name": name,
            "price": price if price > 0 else None
        }

        try:
            response = requests.post(f"{API_URL}/products/", json=payload)

            if response.ok:
                st.success("Produto cadastrado!")
            else:
                st.error(f"Erro ao cadastrar: {response.text}")
        except Exception as e:
            st.error(f"Erro ao conectar ao backend: {e}")


# ============================
# LISTAR FUNCIONÁRIOS
# ============================

try:
    employees = requests.get(f"{API_URL}/employees/").json()
    employees_names = {e["name"]: e["id"] for e in employees}
except:
    employees = []
    employees_names = {}


# ============================
# CADASTRAR COMPRA
# ============================

st.header("Cadastrar Compra")

# Carregar produtos da API
try:
    products = requests.get(f"{API_URL}/products/").json()
    product_names = {p["name"]: p["id"] for p in products}
except:
    products = []
    product_names = {}

with st.form("purchase_form"):
    if store_names:
        purchase_store = st.selectbox("Selecione a Loja", list(store_names.keys()))
    else:
        st.warning("Cadastre uma loja primeiro.")
        purchase_store = None

    if employees_names:
        employee_name = st.selectbox("Selecione o funcionário", list(employees_names.keys()))
    else:
        st.warning("Cadastre um funcionário primeiro.")
        employee_name = None

    if product_names:
        product_name = st.selectbox("Selecione o Produto", list(product_names.keys()))
    else:
        st.warning("Cadastre um produto primeiro.")
        product_name = None

    amount = st.number_input("Valor da Compra", min_value=0.0)

    submit_purchase = st.form_submit_button("Cadastrar Compra")

    if submit_purchase:
        if not (purchase_store and employee_name and product_name):
            st.error("Todos os campos são obrigatórios.")
        else:
            payload = {
                "store_id": store_names[purchase_store],
                "employee_id": employees_names[employee_name],
                "product_id": product_names[product_name],
                "amount": amount
            }

            response = requests.post(f"{API_URL}/purchases/", json=payload)

            if response.ok:
                st.success("Compra cadastrada!")
            else:
                st.error(f"Erro: {response.text}")
