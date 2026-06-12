from fastapi import APIRouter,HTTPException,status,Depends
from app.models.admin import Admin
from app.schemas.admin import AdminLogin
from app.database import get_db
from app.core.security import create_access_token,verify_password
from sqlalchemy.orm import Session
router=APIRouter()

@router.post("/auth/login")
def login(form: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == form.email).first()
    
    if not admin or not verify_password(form.password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    token = create_access_token(data={"sub": admin.email})
    
    return {"access_token": token, "token_type": "bearer"}

    

    

 





    
    
    

    


    



