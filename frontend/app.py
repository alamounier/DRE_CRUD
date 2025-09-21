import streamlit as st
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

st.title("Sales CRUD Simulator")

menu = ["Create Sale", "View Sales"]
choice = st.sidebar.selectbox("Menu", menu)

# ------------------ CREATE SALE ------------------
if choice == "Create Sale":
    st.subheader("Create a new sale")

    customers_resp = requests.get(f"{API_URL}/customers/")
    stores_resp = requests.get(f"{API_URL}/stores/")

    customer_options = {c["customer_id"]: c["name"] for c in customers_resp.json()} if customers_resp.status_code == 200 else {}
    store_options = {s["store_code"]: s["store_name"] for s in stores_resp.json()} if stores_resp.status_code == 200 else {}

    customer_id = st.selectbox("Customer", options=list(customer_options.keys()), format_func=lambda x: customer_options[x])
    store_code = st.selectbox("Store", options=list(store_options.keys()), format_func=lambda x: store_options[x])

    sale_amount = st.number_input("Sale Amount", min_value=0.0)
    payment_method = st.selectbox("Payment Method", ["Credit", "Debit", "Pix", "Cash"])
    installments = st.number_input("Installments", min_value=1, max_value=12, value=1)
    sale_date = st.date_input("Sale Date", datetime.today())

    if payment_method == "Credit": payment_method_code = 1
    elif payment_method == "Debit": payment_method_code = 2
    elif payment_method == "Pix": payment_method_code = 3
    elif payment_method == "Cash": payment_method_code = 4

    sales_category = st.selectbox(
        "Sales Category",
        options=[1, 2],
        format_func=lambda x: "In Person" if x == 1 else "Online"
    )

    if st.button("Create"):
        payload = {
            "customer_id": customer_id,
            "store_code": store_code,
            "sale_date": str(sale_date),
            "sale_amount": sale_amount,
            "tax_amount": sale_amount * 0.15,
            "payment_method": payment_method_code,
            "installments": installments,
            "sales_category": sales_category
        }
        response = requests.post(f"{API_URL}/sales/", json=payload)
        if response.status_code == 200:
            st.success("Sale created successfully!")
            st.json(response.json())
        else:
            st.error(f"Error creating sale: {response.text}")

# ------------------ VIEW SALES ------------------
if choice == "View Sales":
    st.subheader("Sales List")
    response = requests.get(f"{API_URL}/sales/")
    if response.status_code == 200:
        sales = response.json()
        st.write(sales)
    else:
        st.error("Could not fetch sales.")
