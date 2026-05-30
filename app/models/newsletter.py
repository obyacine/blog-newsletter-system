from sqlalchemy import Column, String,Boolean,Integer,DateTime
from app.database import Base

class Newsletter(Base):
    __tablename__="newsletter"

    id=Column(Integer,primary_key=True,index=True)
    subject=Column(String,nullable=False)
    body=Column(String(255))
    sent_at=Column(DateTime)
    recipients_count=Column(Integer)

    




