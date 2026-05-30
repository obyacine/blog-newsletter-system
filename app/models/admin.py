from sqlalchemy import  Column,Integer,String,Boolean,DateTime
from app.database import Base

class Admin(Base):
    __tablename__="admin"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True , index=True)
    hashed_password=Column(String)

