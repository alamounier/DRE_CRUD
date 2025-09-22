from pydantic import BaseModel

class StoreBase(BaseModel):
    name: str
    city: str

class Store(StoreBase):
    id: int
    class Config:
        orm_mode = True

class PurchaseBase(BaseModel):
    store_id: int
    product_name: str
    amount: float

class Purchase(PurchaseBase):
    id: int
    class Config:
        orm_mode = True
