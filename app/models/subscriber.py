from sqlalchemy import Column,Integer,String,Boolean,DateTime
from app.database import Base

class Subscriber(Base):
    __tablename__ ="subscriber"
    id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String,nullable=False)
    last_name=Column(String,nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    is_active=Column(Boolean)
    subscribed_at=Column(DateTime)

    

