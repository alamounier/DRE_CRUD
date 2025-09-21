from faker import Faker
import random
import pandas as pd
from datetime import datetime
from .database import SessionLocal
from .models import Customer, Store

fake = Faker("pt_BR")

class SampleDataGenerator:
    def __init__(self):
        self.fake = fake

    def seed_customers(self, n_customers=50):
        """Gera clientes brasileiros"""
        db = SessionLocal()

        # Evita duplicação
        if db.query(Customer).first():
            db.close()
            return

        for i in range(1, n_customers + 1):
            customer = Customer(
                customer_id=f"CUST_{i:05}",
                name=self.fake.name(),
                ssn=self.fake.cpf().replace(".", "").replace("-", ""),  # CPF válido
                email=self.fake.email(),
                phone=f"+55 {self.fake.msisdn()[2:]}",
                birth_date=self.fake.date_of_birth(minimum_age=18, maximum_age=80),
                city=self.fake.city(),
                state=self.fake.estado_sigla()
            )
            db.add(customer)

        db.commit()
        db.close()

    def seed_stores(self, n_stores=23):
        """Gera lojas com base nas principais cidades brasileiras"""
        db = SessionLocal()

        if db.query(Store).first():
            db.close()
            return

        store_codes = [f"STORE_{i:03d}" for i in range(1, n_stores + 1)]

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

        for code in store_codes:
            sales_area_m2 = random.randint(200, 2000)
            num_employees = max(2, sales_area_m2 // 400)
            employee_cost = num_employees * cost_per_employee
            store_weight = round(random.uniform(1, 2.0), 2)

            chosen_city = random.choice(brazilian_cities)

            store = Store(
                store_code=code,
                store_name=self.fake.company(),
                street=self.fake.street_name(),
                number=random.randint(10, 9999),
                complement=random.choice(["", "Store A", "Store B", "Block 1", "2nd Floor"]),
                district=self.fake.city_suffix(),
                city=chosen_city["city"],
                state=chosen_city["state"],
                country="Brazil",
                postal_code=self.fake.postcode().replace("-", "").zfill(8),
                country_code="55",
                phone=f"({random.randint(10, 99)}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                manager=self.fake.name(),
                sales_area_m2=sales_area_m2,
                num_employees=num_employees,
                monthly_employee_cost=employee_cost,
                store_weight=store_weight,
                latitude=chosen_city["latitude"],
                longitude=chosen_city["longitude"],
                created_at=datetime.now(),
                updated_at=None
            )
            db.add(store)

        db.commit()
        db.close()

def seed_data():
    generator = SampleDataGenerator()
    generator.seed_customers()
    generator.seed_stores()
