from sqlalchemy import Column,Integer,String,Boolean,DateTime
from app.database import Base

class Article(Base):
    __tablename__="article"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    slug=Column(String,unique=True)
    author=Column(String)
    content=Column(String)
    created_at=Column(DateTime)
    is_published=Column(Boolean,default=False)


   
