from fastapi import APIRouter, HTTPException, Depends,status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleResponse

router = APIRouter()

@router.post("/admin/article")

def create_article(form:ArticleCreate, db:Session=Depends(get_db)):
    new_article=Article(
        title=form.title,
        author=form.author,
        slug=form.slug,
        content=form.content,
        is_published=datetime.utcnow

    )

    
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    
    return new_article



@router.put("/admin/articles/{id}")


def update_article(id: int, form: ArticleCreate, db: Session = Depends(get_db)):

    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    article.title = form.title
    article.slug = form.slug
    article.content = form.content
    db.commit()
    db.refresh(article)
    return article

@router.delete("/admin/articles/{id}")

def delete_article(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    db.delete(article)
    db.commit()
    return {"message": "Article supprimé"}



@router.post("/admin/articles/{id}/publish")

def toggle_publish(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    article.is_published = not article.is_published
    db.commit()
    db.refresh(article)
    return article
    
    

   
    

    


    