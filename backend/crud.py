from sqlalchemy.orm import Session
from models import Store, Purchase, Employee, Product
from schemas import StoreBase, PurchaseBase, EmployeeBase, ProductBase

# ---------------- STORES ----------------

def get_stores(db: Session):
    return db.query(Store).all()

def get_store(db: Session, store_id: int):
    return db.query(Store).filter(Store.id == store_id).first()

def create_store(db: Session, store: StoreBase):
    db_store = Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def update_store(db: Session, store_id: int, store: StoreBase):
    db_store = get_store(db, store_id)
    if not db_store:
        return None
    for field, value in store.dict().items():
        setattr(db_store, field, value)
    db.commit()
    db.refresh(db_store)
    return db_store

def delete_store(db: Session, store_id: int):
    db_store = get_store(db, store_id)
    if not db_store:
        return False
    db.delete(db_store)
    db.commit()
    return True


# ---------------- PURCHASES ----------------

def get_purchases(db: Session):
    return db.query(Purchase).all()

def get_purchase(db: Session, purchase_id: int):
    return db.query(Purchase).filter(Purchase.id == purchase_id).first()

def create_purchase(db: Session, purchase: PurchaseBase):
    db_purchase = Purchase(**purchase.dict())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

def update_purchase(db: Session, purchase_id: int, purchase: PurchaseBase):
    db_purchase = get_purchase(db, purchase_id)
    if not db_purchase:
        return None
    for field, value in purchase.dict().items():
        setattr(db_purchase, field, value)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

def delete_purchase(db: Session, purchase_id: int):
    db_purchase = get_purchase(db, purchase_id)
    if not db_purchase:
        return False
    db.delete(db_purchase)
    db.commit()
    return True


# ---------------- EMPLOYEES ----------------

def get_employees(db: Session):
    return db.query(Employee).all()

def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

def create_employee(db: Session, employee: EmployeeBase):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee: EmployeeBase):
    db_emp = get_employee(db, employee_id)
    if not db_emp:
        return None
    for field, value in employee.dict().items():
        setattr(db_emp, field, value)
    db.commit()
    db.refresh(db_emp)
    return db_emp

def delete_employee(db: Session, employee_id: int):
    db_emp = get_employee(db, employee_id)
    if not db_emp:
        return False
    db.delete(db_emp)
    db.commit()
    return True


# ---------------- PRODUCTS ----------------

def get_products(db: Session):
    return db.query(Product).all()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db: Session, product: ProductBase):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductBase):
    db_prod = get_product(db, product_id)
    if not db_prod:
        return None
    for field, value in product.dict().items():
        setattr(db_prod, field, value)
    db.commit()
    db.refresh(db_prod)
    return db_prod

def delete_product(db: Session, product_id: int):
    db_prod = get_product(db, product_id)
    if not db_prod:
        return False
    db.delete(db_prod)
    db.commit()
    return True
