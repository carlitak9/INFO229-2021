from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base #Se importa el objeto Base desde el archivo database.py

class News(Base): 

    __tablename__ = "news"

    id_news = Column(Integer, primary_key=True, index=True)
    title = Column(String(400))
    url = Column(String(400))
    date = Column(String(50))
    media_outlet = Column(String(400))
    category =  Column(String(50))
