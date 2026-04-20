from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from utils.hashing import verify_password, hash_password
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

from typing import Optional, Any

class UserSignup(BaseModel):
    name: Optional[str] = None
    email: str
    password: str
    phone: Optional[Any] = None
    age: Optional[Any] = None
    location: Optional[Any] = None
    village: Optional[Any] = None

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return {"message": "Login successful", "user_id": user.id, "role": user.role}

@router.post("/signup/patient")
def signup_patient(user_data: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user_data.email,
        full_name=user_data.name,
        phone=str(user_data.phone) if user_data.phone else None,
        password_hash=hash_password(user_data.password),
        role="patient"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Patient created", "user_id": new_user.id}

@router.post("/signup/doctor")
def signup_doctor(user_data: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user_data.email,
        full_name=user_data.name,
        phone=str(user_data.phone) if user_data.phone else None,
        password_hash=hash_password(user_data.password),
        role="doctor"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Doctor created", "user_id": new_user.id}
