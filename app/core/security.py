from passlib.context import CryptContext
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.admin import Admin


pwd_context = CryptContext(schemes=["bcrypt"])


def hashpassword(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="token invalide")
    return email


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        email = verify_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="token invalide ou expiré")

    admin = db.query(Admin).filter(Admin.email == email).first()
    if admin is None:
        raise HTTPException(status_code=401, detail="admin non trouvé")

    return admin