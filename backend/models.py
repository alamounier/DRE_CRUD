from sqlalchemy import Column, String, Float, Integer, Date
from backend.database import Base

class Store(Base):
    __tablename__ = "stores"
    store_code = Column(String, primary_key=True, index=True)
    store_name = Column(String)

class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(String, primary_key=True, index=True)
    name = Column(String)

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
