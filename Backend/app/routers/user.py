# app/routers/example.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.user_models import User, Integration
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timezone
from app.services.security import encrypt


router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schemas
class IntegrationCreate(BaseModel):
    provider: str
    token: str
    base_url: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    integrations: Optional[List[IntegrationCreate]] = []

@router.post("/addUser")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists.")

    # Create new user
    new_user = User(email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Add integrations (optional)
    for integ in user.integrations:
        integration = Integration(
            user_id=new_user.id,
            provider=integ.provider,
            token_encrypted=encrypt(integ.token),  # 🔒 you should encrypt this!
            base_url=integ.base_url,
            created_at=datetime.now(timezone.utc)
        )
        db.add(integration)

    db.commit()

    return {"message": "User and integrations added successfully."}

@router.get("/getUserIntegrations/{user_id}")
def get_user_integrations(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    integrations = db.query(Integration).filter_by(user_id=user_id).all()
    return {
        "user_id": user.id,
        "email": user.email,
        "integrations": [
            {
                "provider": integ.provider,
                "base_url": integ.base_url,
                "created_at": integ.created_at.isoformat()
            } for integ in integrations
        ]
    }
