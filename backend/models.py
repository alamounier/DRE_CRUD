# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    city = Column(String)
    state = Column(String)
    store_code = Column(String)
    square_meter = Column(Float)

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    store_id = Column(Integer) 
    salary = Column(Float)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=True)

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    amount = Column(Float)

