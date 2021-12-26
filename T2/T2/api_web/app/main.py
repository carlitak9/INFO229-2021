from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from fastapi_pagination import Page, add_pagination, paginate


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/news/", response_model=schemas.News)
def create_news(news: schemas.News, db: Session = Depends(get_db)):
    return crud.create_news(db=db, news=news)

@app.get("/news/", response_model=List[schemas.News])
def read_all_news(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    news = crud.get_all_news(db, skip=skip, limit=limit)
    return news

@app.get("/v1/news/", response_model=List[schemas.News])
def read_news(from_: str="2021-10-01", to_: str = "2021-10-30", category: str="", db: Session = Depends(get_db) ):
    news = crud.get_news(db, from_=from_, to_=to_,category=category)
    
    return news
