from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.dependencies import get_current_user
from app.models import User
from app.schemas import TokenOut, UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    email = str(payload.email).lower()
    existing_user = db.scalar(select(User).where(User.email == email))

    if existing_user:
        raise HTTPException(409, "Este correo ya está registrado")

    user = User(
        name=payload.name,
        email=email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenOut)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.scalar(select(User).where(User.email == form.username.lower()))

    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Correo o contraseña incorrectos")

    return {
        "access_token": create_access_token(str(user.id)),
        "user": user,
    }


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
