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
    sales_category: int   # 1 = In Person, 2 = Online

class SaleCreate(SaleBase):
    pass

class SaleUpdate(BaseModel):
    sale_amount: float | None = None
    tax_amount: float | None = None
    payment_method: int | None = None
    installments: int | None = None
    sales_category: int | None = None

class Sale(SaleBase):
    sale_id: str
    class Config:
        orm_mode = True
