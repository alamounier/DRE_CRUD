from sqlalchemy.orm import Session
from . import models, schemas

def get_stores(db: Session):
    return db.query(models.Store).all()

def create_store(db: Session, store: schemas.StoreBase):
    db_store = models.Store(name=store.name, city=store.city)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def get_purchases(db: Session):
    return db.query(models.Purchase).all()

def create_purchase(db: Session, purchase: schemas.PurchaseBase):
    db_purchase = models.Purchase(**purchase.dict())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase
