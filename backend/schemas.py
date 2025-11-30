from pydantic import BaseModel

class StoreBase(BaseModel):
    name: str
    city: str
    state: str
    store_code: str
    square_meter: float

class Store(StoreBase):
    id: int
    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    store_id: int
    name: str
    salary: float

class Employee(EmployeeBase):
    id: int
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    category: str
    name: str
    price: float = None

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class PurchaseBase(BaseModel):
    store_id: int
    employee_id: int
    product_id: int
    amount: float

class Purchase(PurchaseBase):
    id: int

    class Config:
        orm_mode = True


