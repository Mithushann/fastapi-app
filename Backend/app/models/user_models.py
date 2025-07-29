from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.db import Base
from datetime import datetime, timezone

# app/models/user_models.py
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)

    integrations = relationship("Integration", back_populates="user")
    
class Integration(Base):
    __tablename__ = "user_integrations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    provider = Column(String)
    token_encrypted = Column(String, nullable=False)
    base_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="integrations")