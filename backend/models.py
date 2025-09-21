from sqlalchemy import Column, String, Float, Integer, Date, ForeignKey
from backend.database import Base

class Store(Base):
    __tablename__ = "stores"
    store_code = Column(String, primary_key=True, index=True)
    store_name = Column(String)
    street = Column(String)
    number = Column(Integer)
    complement = Column(String)
    district = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postal_code = Column(String)
    country_code = Column(Integer)
    phone = Column(String)
    manager = Column(String)
    sales_area_m2 = Column(Integer)
    num_employees = Column(Integer)
    monthly_employee_cost = Column(Float)
    store_weight = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(Date)
    updated_at = Column(Date, nullable=True)

class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    ssn = Column(String, unique=True)
    email = Column(String, unique=True)
    phone = Column(String)
    birth_date = Column(Date)
    city = Column(String)
    state = Column(String)

class Sale(Base):
    __tablename__ = "sales"
    sale_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String)
    store_code = Column(String)
    sale_date = Column(Date)
    sale_amount = Column(Float)
    tax_amount = Column(Float)
    payment_method = Column(Integer)
    installments = Column(Integer)
    sales_category = Column(Integer)  # 1 = In Person, 2 = Online
