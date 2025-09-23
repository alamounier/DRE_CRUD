from sqlalchemy import Column, Integer, String, Float
from database import Base

class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    city = Column(String)

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer)
    product_name = Column(String)
    amount = Column(Float)
