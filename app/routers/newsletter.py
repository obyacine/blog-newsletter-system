from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.subscriber import Subscriber
from app.models.newsletter import Newsletter
from app.schemas.subscriber import SubscriberCreate, SubscriberResponse
from app.schemas.newsletter import NewsletterCreate, NewsletterResponse

router = APIRouter()



@router.post("/subscribe")
def subscribe(form: SubscriberCreate, db: Session = Depends(get_db)):
    existing = db.query(Subscriber).filter(Subscriber.email == form.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email déjà abonné")

    new_subscriber = Subscriber(
        first_name=form.first_name,
        last_name=form.last_name,
        email=form.email,
        is_active=True,
        subscribed_at=datetime.utcnow()
    )
    db.add(new_subscriber)
    db.commit()
    db.refresh(new_subscriber)
    return new_subscriber


@router.get("/unsubscribe/{email}")
def unsubscribe(email: str, db: Session = Depends(get_db)):
    subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
    if not subscriber:
        raise HTTPException(status_code=404, detail="Abonné non trouvé")

    subscriber.is_active = False
    db.commit()
    return {"message": "Désabonnement réussi"}



@router.get("/admin/subscribers")
def get_subscribers(db: Session = Depends(get_db)):
    subscribers = db.query(Subscriber).filter(Subscriber.is_active == True).all()
    return subscribers


@router.post("/admin/newsletter/send")
def send_newsletter(form: NewsletterCreate, db: Session = Depends(get_db)):
    subscribers = db.query(Subscriber).filter(Subscriber.is_active == True).all()

    # ici on appellera plus tard email_service pour envoyer les emails
    recipients_count = len(subscribers)

    new_newsletter = Newsletter(
        subject=form.subject,
        body=form.body,
        sent_at=datetime.utcnow(),
        recipients_count=recipients_count
    )
    db.add(new_newsletter)
    db.commit()
    db.refresh(new_newsletter)
    return new_newsletter


@router.get("/admin/newsletter/history")
def get_newsletter_history(db: Session = Depends(get_db)):
    history = db.query(Newsletter).order_by(Newsletter.sent_at.desc()).all()
    return history