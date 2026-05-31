from pydantic import BaseModel,EmailStr
from datetime import datetime

class SubscriberCreate(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr


class SubscriberResponse(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:EmailStr
    is_active:bool
    subscribed_at:datetime


    class Config:
        from_attributes=True


