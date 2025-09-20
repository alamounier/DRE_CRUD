from pydantic import BaseModel
from datetime import date

class SaleBase(BaseModel):
    customer_id: str
    store_code: str
    sale_date: date
    sale_amount: float
    tax_amount: float
    payment_method: int
    installments: int

class SaleCreate(SaleBase):
    pass

class SaleUpdate(BaseModel):
    sale_amount: float = None
    tax_amount: float = None
    payment_method: int = None
    installments: int = None

class Sale(SaleBase):
    sale_id: str
    class Config:
        orm_mode = True
