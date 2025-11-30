from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import (
    Store, StoreBase,
    Purchase, PurchaseBase,
    Employee, EmployeeBase,
    Product, ProductBase
)
from crud import (
    get_stores, get_store, create_store, update_store, delete_store,
    get_purchases, get_purchase, create_purchase, update_purchase, delete_purchase,
    get_employees, get_employee, create_employee, update_employee, delete_employee,
    get_products, get_product, create_product, update_product, delete_product
)

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Backend está rodando 🚀"}

# ---------- STORES ----------

@router.get("/stores/", response_model=list[Store])
def read_stores(db: Session = Depends(get_db)):
    return get_stores(db)

@router.post("/stores/", response_model=Store)
def add_store(store: StoreBase, db: Session = Depends(get_db)):
    return create_store(db, store)

@router.put("/stores/{store_id}", response_model=Store)
def modify_store(store_id: int, store: StoreBase, db: Session = Depends(get_db)):
    updated = update_store(db, store_id, store)
    if not updated:
        raise HTTPException(404, "Store not found")
    return updated

@router.delete("/stores/{store_id}")
def remove_store(store_id: int, db: Session = Depends(get_db)):
    deleted = delete_store(db, store_id)
    if not deleted:
        raise HTTPException(404, "Store not found")
    return {"message": "Deleted successfully"}

# ---------- PURCHASES ----------

@router.get("/purchases/", response_model=list[Purchase])
def read_purchases(db: Session = Depends(get_db)):
    return get_purchases(db)

@router.post("/purchases/", response_model=Purchase)
def add_purchase(purchase: PurchaseBase, db: Session = Depends(get_db)):
    return create_purchase(db, purchase)

@router.put("/purchases/{purchase_id}", response_model=Purchase)
def modify_purchase(purchase_id: int, purchase: PurchaseBase, db: Session = Depends(get_db)):
    updated = update_purchase(db, purchase_id, purchase)
    if not updated:
        raise HTTPException(404, "Purchase not found")
    return updated

@router.delete("/purchases/{purchase_id}")
def remove_purchase(purchase_id: int, db: Session = Depends(get_db)):
    deleted = delete_purchase(db, purchase_id)
    if not deleted:
        raise HTTPException(404, "Purchase not found")
    return {"message": "Deleted successfully"}

# ---------- EMPLOYEES ----------

@router.get("/employees/", response_model=list[Employee])
def read_employees(db: Session = Depends(get_db)):
    return get_employees(db)

@router.post("/employees/", response_model=Employee)
def add_employee(employee: EmployeeBase, db: Session = Depends(get_db)):
    return create_employee(db, employee)

@router.put("/employees/{employee_id}", response_model=Employee)
def modify_employee(employee_id: int, employee: EmployeeBase, db: Session = Depends(get_db)):
    updated = update_employee(db, employee_id, employee)
    if not updated:
        raise HTTPException(404, "Employee not found")
    return updated

@router.delete("/employees/{employee_id}")
def remove_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = delete_employee(db, employee_id)
    if not deleted:
        raise HTTPException(404, "Employee not found")
    return {"message": "Deleted successfully"}

# ---------- PRODUCTS ----------

@router.get("/products/", response_model=list[Product])
def read_products(db: Session = Depends(get_db)):
    return get_products(db)

@router.post("/products/", response_model=Product)
def add_product(product: ProductBase, db: Session = Depends(get_db)):
    return create_product(db, product)

@router.put("/products/{product_id}", response_model=Product)
def modify_product(product_id: int, product: ProductBase, db: Session = Depends(get_db)):
    updated = update_product(db, product_id, product)
    if not updated:
        raise HTTPException(404, "Product not found")
    return updated

@router.delete("/products/{product_id}")
def remove_product(product_id: int, db: Session = Depends(get_db)):
    deleted = delete_product(db, product_id)
    if not deleted:
        raise HTTPException(404, "Product not found")
    return {"message": "Deleted successfully"}
