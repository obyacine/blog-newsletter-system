from pydantic import BaseModel,EmailStr
from datetime import datetime

class AdminLogin(BaseModel):
    email:EmailStr
    password:str



class AdminResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    
class config:
  from_attributes = True
    
