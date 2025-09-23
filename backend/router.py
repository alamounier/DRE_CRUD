from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas import Store, Purchase, StoreBase, PurchaseBase
from crud import (
    get_stores,
    get_purchases,
    create_store,
    create_purchase
)
 
router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Backend está rodando 🚀"}

@router.get("/stores/", response_model=list[Store])
def read_stores(db: Session = Depends(get_db)):
    return get_stores(db)

@router.post("/stores/", response_model=Store)
def add_store(store: StoreBase, db: Session = Depends(get_db)):
    return create_store(db, store)

@router.get("/purchases/", response_model=list[Purchase])
def read_purchases(db: Session = Depends(get_db)):
    return get_purchases(db)

@router.post("/purchases/", response_model=Purchase)
def add_purchase(purchase: PurchaseBase, db: Session = Depends(get_db)):
    return create_purchase(db, purchase)
