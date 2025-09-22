from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/stores/", response_model=list[schemas.Store])
def read_stores(db: Session = Depends(get_db)):
    return crud.get_stores(db)

@app.post("/stores/", response_model=schemas.Store)
def add_store(store: schemas.StoreBase, db: Session = Depends(get_db)):
    return crud.create_store(db, store)

@app.get("/purchases/", response_model=list[schemas.Purchase])
def read_purchases(db: Session = Depends(get_db)):
    return crud.get_purchases(db)

@app.post("/purchases/", response_model=schemas.Purchase)
def add_purchase(purchase: schemas.PurchaseBase, db: Session = Depends(get_db)):
    return crud.create_purchase(db, purchase)