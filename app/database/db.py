# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Load DB URL from environment variable or fallback to local SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# SQLite needs this argument, Postgres does not
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# SessionLocal: used to interact with the DB in endpoints
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: used for models
Base = declarative_base()