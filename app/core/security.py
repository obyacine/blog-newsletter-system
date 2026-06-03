from passlib.context import CryptContext
from jose import jwt
from app.core.config import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime,timedelta
from fastapi import HTTPException,status

pwd_context = CryptContext(schemes=["bcrypt"])


def hashpassword(password:str)->str:
 return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



def create_access_token(data:dict)->str:
   to_encode=data.copy()
   expire=datetime.utcnow()+timedelta(minutes=30)
   to_encode.update({"exp":expire})
   return jwt.encode(to_encode,SECRET_KEY,algorithms=ALGORITHM)

def verify_token(token:str)->str:
   payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
   email=payload.get("sub")
   if email is None:
      raise HTTPException(status_code=401 , detail="token invalide")
   else:
      return email
   
   



