from faker import Faker
from backend.database import SessionLocal, Base, engine
from backend.models import Store, Customer

Base.metadata.create_all(bind=engine)
fake = Faker("pt_BR")
db = SessionLocal()

# Gerar lojas
for i in range(10):
    store = Store(
        store_code=f"STORE_{i+1:03d}",
        store_name=fake.company()
    )
    db.merge(store)

# Gerar clientes
for i in range(20):
    customer = Customer(
        customer_id=f"CUST_{i+1:05d}",
        name=fake.name()
    )
    db.merge(customer)

db.commit()
db.close()
print("✅ Sample stores and customers generated.")
