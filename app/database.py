
from sqlalchemy import create_engine,Column,Integer,String #crée une connexion physique avec la bdd
from sqlalchemy.ext.declarative import declarative_base #base mère c'est une classe mére 
from sqlalchemy.orm import sessionmaker #conversation avec la bdd
from app.core.config import DATABASE_URL #importer database url depuis le fichier .env


engine=create_engine(DATABASE_URL,connect_args={"check_same_thread": False})#connecter mon code python a sqlite

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

