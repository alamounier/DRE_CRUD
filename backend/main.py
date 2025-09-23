from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine,SessionLocal
from router import router
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)