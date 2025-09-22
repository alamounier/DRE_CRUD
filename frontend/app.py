import streamlit as st
import os
import requests

API_URL = os.getenv("API_URL", "http://backend:8000")

st.title("Cadastro de Lojas e Compras")

# Cadastrar loja
st.header("Cadastrar Loja")
with st.form("store_form"):
    name = st.text_input("Nome da Loja")
    city = st.text_input("Cidade")
    submitted = st.form_submit_button("Cadastrar")
    if submitted:
        payload = {"name": name, "city": city}
        response = requests.post(f"{API_URL}/stores/", json=payload)
        if response.ok:
            st.success("Loja cadastrada!")
        else:
            st.error(f"Erro: {response.text}")

# Listar lojas
try:
    stores = requests.get(f"{API_URL}/stores/").json()
except:
    stores = []

store_names = {store['name']: store['id'] for store in stores}

# Cadastrar compra
st.header("Cadastrar Compra")
with st.form("purchase_form"):
    store_name = st.selectbox("Selecione a Loja", list(store_names.keys()))
    product_name = st.text_input("Produto")
    amount = st.number_input("Valor", min_value=0.0)
    submitted = st.form_submit_button("Cadastrar Compra")
    if submitted:
        payload = {"store_id": store_names[store_name], "product_name": product_name, "amount": amount}
        response = requests.post(f"{API_URL}/purchases/", json=payload)
        if response.ok:
            st.success("Compra cadastrada!")
        else:
            st.error(f"Erro: {response.text}")
