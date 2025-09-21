from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
import uuid

from backend.database import get_db, Base, engine
from backend import models
from backend.models import Sale

Base.metadata.create_all(bind=engine)

app = FastAPI()

class SaleCreateSchema(BaseModel):
    customer_id: str
    store_code: str
    sale_date: date
    sale_amount: float
    tax_amount: float
    payment_method: int
    installments: int
    sales_category: int

@app.get("/customers/")
def list_customers(db: Session = Depends(get_db)):
    return [{"customer_id": c.customer_id, "name": c.name} for c in db.query(models.Customer).all()]

@app.get("/stores/")
def list_stores(db: Session = Depends(get_db)):
    return [{"store_code": s.store_code, "store_name": s.store_name} for s in db.query(models.Store).all()]

@app.post("/sales/")
def create_sale(sale: SaleCreateSchema, db: Session = Depends(get_db)):
    new_sale = Sale(
        sale_id=str(uuid.uuid4()),
        customer_id=sale.customer_id,
        store_code=sale.store_code,
        sale_date=sale.sale_date,
        sale_amount=sale.sale_amount,
        tax_amount=sale.tax_amount,
        payment_method=sale.payment_method,
        installments=sale.installments,
        sales_category=sale.sales_category
    )
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale

@app.get("/sales/")
def list_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()
