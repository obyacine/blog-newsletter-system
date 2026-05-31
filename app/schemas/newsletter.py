from pydantic import BaseModel
from datetime import datetime

class NewsletterCreate(BaseModel):
    subject:str
    body:str
    recipients_count:int


class NewsletterResponse(BaseModel):
    id:int
    subject:str
    body:str
    sent_at:datetime
    recipients_count:int


class config:
    from_attributes=True