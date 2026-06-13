from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.article import Article
from app.schemas.article import ArticleResponse

router=APIRouter()

@router.get("/articles")

def get_articles(db:Session=Depends(get_db)):
    all_articles=db.query(Article).filter(Article.is_published==True).all()

    return all_articles
        

@router.get("/articles/{slug}")

def public_blog(slug:str,db:Session=Depends(get_db)):

    article=db.query(Article).filter(Article.slug==slug).first()

    if not article :
        raise HTTPException(status_code=404, detail="blog not found")
    
    return article




    
        
    






    
 






    

    




