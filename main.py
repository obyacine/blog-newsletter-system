from fastapi import FastAPI
from app.database import Base, engine
from app.routers import public_blog, admin_blog, newsletter, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(public_blog.router)
app.include_router(admin_blog.router)
app.include_router(newsletter.router)
app.include_router(auth.router)