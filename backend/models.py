from sqlalchemy import Column, String, Integer, Float, Date, DateTime
from sqlalchemy.sql import func
from .database import Base

# Customers
class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ssn = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)


# Stores
class Store(Base):
    __tablename__ = "stores"

    store_code = Column(String, primary_key=True, index=True)
    store_name = Column(String, nullable=False)
    street = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    complement = Column(String, nullable=True)
    district = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    manager = Column(String, nullable=False)
    sales_area_m2 = Column(Integer, nullable=False)
    num_employees = Column(Integer, nullable=False)
    monthly_employee_cost = Column(Float, nullable=False)
    store_weight = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


# Sales
class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, nullable=False)
    store_code = Column(String, nullable=False)
    sale_date = Column(Date, nullable=False)
    sale_amount = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=False)
    payment_method = Column(Integer, nullable=False)
    installments = Column(Integer, nullable=False)
    sales_category = Column(Integer, nullable=False)  # 1 = In Person, 2 = Online

