from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='/api/auth/login')
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db))->User:
 subject=decode_access_token(token)
 if not subject: raise HTTPException(401,'Token inválido o vencido')
 user=db.get(User,int(subject))
 if not user: raise HTTPException(401,'Usuario no encontrado')
 return user
def require_admin(user:User=Depends(get_current_user))->User:
 if user.role!='admin': raise HTTPException(403,'Se requiere rol administrador')
 return user
