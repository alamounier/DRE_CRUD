from sqlalchemy.orm import Session
from schemas import StoreBase, PurchaseBase
from models import Store, Purchase

def get_stores(db: Session):
    return db.query(Store).all()

def create_store(db: Session, store: StoreBase):
    db_store = Store(name=store.name, city=store.city)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def get_purchases(db: Session):
    return db.query(Purchase).all()

def create_purchase(db: Session, purchase: PurchaseBase):
    db_purchase = Purchase(**purchase.dict())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase
