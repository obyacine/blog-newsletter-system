from pydantic import BaseModel
from datetime import datetime

class ArticleCreate(BaseModel):
    title:str
    slug:str
    author:str
    content:str
    is_published:bool


class ArticleResponse(BaseModel):

    id:int
    title:str
    slug:str
    author:str
    content:str
    created_at:datetime
    is_published:bool
   
   
   
class config:
    from_attributes=True #lire depuis sqlalchemy et convertir les objets en json  




