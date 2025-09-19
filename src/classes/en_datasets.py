import pandas as pd
import random
from faker import Faker
from datetime import timedelta, date


class DatasetGenerator:
    def __init__(self, output_path="files/en"):
        self.fake = Faker("pt_BR")
        self.output_path = output_path
        self.df_stores = None
        self.df_dim_customers = None
        self.df_dim_sales = None
        self.df_fact_receivables = None
        self.df_expenses = None
        self.df_loans = None

    # ---------- GENERATE STORES ----------
    def create_dataset_store(self, n_stores=23):
        store_codes = [f"STORE_{i:03d}" for i in range(1, n_stores + 1)]

        # Main Brazilian cities (with lat/lon)
        brazilian_cities = [
            {"city": "São Paulo", "state": "SP", "latitude": -23.5505, "longitude": -46.6333},
            {"city": "Rio de Janeiro", "state": "RJ", "latitude": -22.9068, "longitude": -43.1729},
            {"city": "Belo Horizonte", "state": "MG", "latitude": -19.9167, "longitude": -43.9345},
            {"city": "Curitiba", "state": "PR", "latitude": -25.4284, "longitude": -49.2733},
            {"city": "Fortaleza", "state": "CE", "latitude": -3.7319, "longitude": -38.5267},
            {"city": "Salvador", "state": "BA", "latitude": -12.9777, "longitude": -38.5016},
            {"city": "Recife", "state": "PE", "latitude": -8.0476, "longitude": -34.8770},
            {"city": "Porto Alegre", "state": "RS", "latitude": -30.0346, "longitude": -51.2177},
            {"city": "Manaus", "state": "AM", "latitude": -3.1190, "longitude": -60.0217},
            {"city": "Goiânia", "state": "GO", "latitude": -16.6869, "longitude": -49.2648},
            {"city": "Campinas", "state": "SP", "latitude": -22.9056, "longitude": -47.0608},
            {"city": "São Luís", "state": "MA", "latitude": -2.5307, "longitude": -44.3068}
        ]

        cost_per_employee = 3000
        store_data = []

        for code in store_codes:
            sales_area_m2 = random.randint(200, 2000)
            num_employees = max(2, sales_area_m2 // 400)
            employee_cost = num_employees * cost_per_employee
            store_weight = round(random.uniform(1, 2.0), 2)

            chosen_city = random.choice(brazilian_cities)

            store_data.append({
                "store_code": code,
                "store_name": self.fake.company(),
                "street": self.fake.street_name(),
                "number": random.randint(10, 9999),
                "complement": random.choice(["", "Store A", "Store B", "Block 1", "2nd Floor"]),
                "district": self.fake.city_suffix(),
                "city": chosen_city["city"],
                "state": chosen_city["state"],
                "country": "Brazil",
                "postal_code": self.fake.postcode().replace("-", "").zfill(8),
                "country_code": 55,
                "phone": f"{random.randint(90000, 99999)}-{random.randint(0, 9999):04d}",
                "manager": self.fake.name(),
                "sales_area_m2": sales_area_m2,
                "num_employees": num_employees,
                "monthly_employee_cost": employee_cost,
                "store_weight": store_weight,
                "latitude": chosen_city["latitude"],
                "longitude": chosen_city["longitude"],
                "created_at": self.fake.date_between(start_date="-2y", end_date="-1y"),
                "updated_at": None
            })

        self.df_stores = pd.DataFrame(store_data)
        self.df_stores["created_at"] = pd.to_datetime(self.df_stores["created_at"])
        self.df_stores.to_csv(f"{self.output_path}/dim_stores.csv", index=False, encoding="utf-8-sig")
        print("✅ File 'dim_stores.csv' generated.")
        return self.df_stores

    # ---------- GENERATE SALES ----------
    def create_dataset_sales(self, n_customers=5000):
        if self.df_stores is None:
            raise ValueError("You need to generate stores first.")

        # Payment methods
        # 1 = Credit (can be installments)
        # 2 = Debit
        # 3 = Pix
        # 4 = Cash
        payment_methods = [1, 2, 3, 4]
        payment_weights = [0.55, 0.25, 0.15, 0.05]

        # Sales categories (1=In-store, 2=Online)
        sales_categories = [1, 2]
        category_weights = [0.7, 0.3]

        # Seasonality (monthly weights)
        seasonality = {
            1: 0.6, 2: 0.7, 3: 0.9, 4: 1.0,
            5: 1.0, 6: 1.1, 7: 1.0, 8: 0.9,
            9: 1.0, 10: 1.2, 11: 1.5, 12: 1.8
        }

        # Create customers
        customers = []
        for i in range(n_customers):
            customers.append({
                "customer_id": f"CUST_{i+1:05d}",
                "name": self.fake.name(),
                "ssn": self.fake.ssn(),
                "email": self.fake.email(),
                "phone": self.fake.phone_number(),
                "birth_date": self.fake.date_of_birth(minimum_age=18, maximum_age=80),
                "city": self.fake.city(),
                "state": self.fake.state_abbr()
            })
        self.df_dim_customers = pd.DataFrame(customers)

        # Output structures
        dim_sales, fact_receivables = [], []

        # Date range
        dates = pd.date_range(
            start=self.df_stores["created_at"].min(),
            end=date.today(),
            freq="MS"
        )

        for month in dates:
            month = pd.Timestamp(month)
            month_num = month.month

            # Ajuste dinâmico dos pesos por mês, mantendo média 70/30 ±5%
            variation = random.uniform(-0.05, 0.05)
            in_store_weight = min(max(0.7 + variation, 0.6), 0.8)  # garante 60% a 80%
            online_weight = 1 - in_store_weight
            category_weights_month = [in_store_weight, online_weight]

            active_stores = self.df_stores[self.df_stores["created_at"] <= month].copy()

            for _, store in active_stores.iterrows():
                expected_sales = int(random.gauss(50 * store["store_weight"] * seasonality[month_num], 10))
                expected_sales = max(expected_sales, 1)

                for _ in range(expected_sales):
                    sale_id = self.fake.uuid4()
                    customer = random.choice(self.df_dim_customers["customer_id"])
                    sale_date = month + timedelta(days=random.randint(0, 27))

                    payment_method = random.choices(payment_methods, weights=payment_weights, k=1)[0]
                    sales_category = random.choices(sales_categories, weights=category_weights_month, k=1)[0]  # <-- aqui

                    sale_amount = round(random.uniform(100, 600) * store["store_weight"], 2)

                    # Installments: only credit
                    if payment_method == 1:  
                        installments = random.choice(range(1, 11))
                    else:
                        installments = 1

                    # Taxes (example: 15%)
                    tax_amount = round(sale_amount * 0.15, 2)

                    # Register sale
                    dim_sales.append({
                        "sale_id": sale_id,
                        "installments": installments,
                        "sale_date": sale_date,
                        "sale_amount": sale_amount,
                        "tax_amount": tax_amount,
                        "payment_method": payment_method,
                        "customer_id": customer,
                        "sales_category": sales_category,
                        "store_code": store["store_code"]
                    })

                    # --- Generate receivables ---
                    if payment_method == 1:  # Credit
                        base_value = round(sale_amount / installments, 2)
                        installment_values = [base_value] * installments
                        diff = round(sale_amount - sum(installment_values), 2)
                        installment_values[-1] += diff

                        for i, value in enumerate(installment_values, 1):
                            fact_receivables.append({
                                "transaction_id": self.fake.uuid4(),
                                "sale_id": sale_id,
                                "receipt_date": sale_date + timedelta(days=30 * i),
                                "receipt_value": value
                            })

                    elif payment_method == 2:  # Debit
                        delay = random.randint(1, 2)
                        fact_receivables.append({
                            "transaction_id": self.fake.uuid4(),
                            "sale_id": sale_id,
                            "receipt_date": sale_date + timedelta(days=delay),
                            "receipt_value": sale_amount
                        })

                    else:  # Pix and Cash = same day
                        fact_receivables.append({
                            "transaction_id": self.fake.uuid4(),
                            "sale_id": sale_id,
                            "receipt_date": sale_date,
                            "receipt_value": sale_amount
                        })

        self.df_dim_sales = pd.DataFrame(dim_sales)
        self.df_fact_receivables = pd.DataFrame(fact_receivables)

        # Export CSVs
        self.df_dim_customers.to_csv(f"{self.output_path}/dim_customers.csv", index=False, encoding="utf-8-sig")
        self.df_dim_sales.to_csv(f"{self.output_path}/dim_sales.csv", index=False, encoding="utf-8-sig")
        self.df_fact_receivables.to_csv(f"{self.output_path}/fact_receivables.csv", index=False, encoding="utf-8-sig")

        print("✅ Files for customers, sales and receivables generated.")
        return self.df_dim_customers, self.df_dim_sales, self.df_fact_receivables

    # ---------- GENERATE EXPENSES ----------
    def create_dataset_expenses(self):
        if self.df_stores is None:
            raise ValueError("You need to generate stores first.")
        if self.df_dim_sales is None:
            raise ValueError("You need to generate sales first.")

        expense_types = ["Rent", "Electricity", "Water", "Internet", "Employee Salaries", "Merchandise"]

        start_date = self.df_stores["created_at"].min()
        end_date = date.today() + pd.DateOffset(months=10)
        dates = pd.date_range(start=start_date, end=end_date, freq="MS")

        expenses = []
        for _, store in self.df_stores.iterrows():
            for month in dates:
                if month < store["created_at"]:
                    continue
                for expense in expense_types:
                    # fixed expenses only up to current month
                    if expense in ["Rent", "Electricity", "Water", "Internet", "Employee Salaries"] and month > pd.Timestamp(date.today().replace(day=1)):
                        continue  

                    if expense == "Merchandise":
                        continue
                    if expense == "Rent":
                        value = round(8 * store["sales_area_m2"] * store["store_weight"], 2)
                    elif expense == "Employee Salaries":
                        value = round(store["num_employees"] * 3000, 2)
                    elif expense == "Electricity":
                        value = round(0.5 * store["sales_area_m2"], 2)
                    elif expense == "Water":
                        value = round(0.2 * store["sales_area_m2"], 2)
                    else:  # Internet
                        value = 150

                    expenses.append({
                        "store_code": store["store_code"],
                        "month_date": month,
                        "expense_type": expense,
                        "expense_value": value
                    })

        for _, sale in self.df_dim_sales.iterrows():
            total_cost = round(sale["sale_amount"] * 0.4, 2)
            installments = 3
            base_value = round(total_cost / installments, 2)
            installment_values = [base_value] * installments
            diff = round(total_cost - sum(installment_values), 2)
            installment_values[-1] += diff

            for i, value in enumerate(installment_values):
                due_date = sale["sale_date"] + pd.DateOffset(months=i)
                expenses.append({
                    "store_code": sale["store_code"],
                    "month_date": due_date,
                    "expense_type": "Merchandise",
                    "expense_value": value
                })

        self.df_expenses = pd.DataFrame(expenses)
        self.df_expenses.to_csv(f"{self.output_path}/fact_expenses.csv", index=False, encoding="utf-8-sig")
        print("✅ File 'fact_expenses.csv' generated.")
        return self.df_expenses

    # ---------- GENERATE LOANS ----------
    def create_dataset_loans(self, annual_interest_rate=0.12, term_months=24):
        if self.df_stores is None:
            raise ValueError("You need to generate stores first.")

        loans = []
        monthly_interest_rate = (1 + annual_interest_rate) ** (1 / 12) - 1

        for _, store in self.df_stores.iterrows():
            loan_value = store["sales_area_m2"] * 50
            contract_date = store["created_at"] - pd.DateOffset(months=3)

            loans.append({
                "store_code": store["store_code"],
                "event_date": contract_date,
                "event_type": "Capital Injection",
                "value": loan_value
            })

            pmt = loan_value * (monthly_interest_rate * (1 + monthly_interest_rate) ** term_months) / (
                (1 + monthly_interest_rate) ** term_months - 1
            )

            for i in range(1, term_months + 1):
                due_date = contract_date + pd.DateOffset(months=i)
                loans.append({
                    "store_code": store["store_code"],
                    "event_date": due_date,
                    "event_type": "Loan Installment",
                    "value": (-1) * round(pmt, 2)
                })

        self.df_loans = pd.DataFrame(loans)
        self.df_loans.to_csv(f"{self.output_path}/fact_loans.csv", index=False, encoding="utf-8-sig")
        print("✅ File 'fact_loans.csv' generated.")
        return self.df_loans
