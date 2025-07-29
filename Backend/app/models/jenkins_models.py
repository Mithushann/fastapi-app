# app/models/jenkins_models.py
from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database.db import Base

class JenkinsBuild(Base):
    __tablename__ = "jenkins_builds"

    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String, index=True)
    build_number = Column(Integer)
    result = Column(String)  # e.g., "SUCCESS", "FAILURE"
    duration_sec = Column(Float)
    timestamp = Column(DateTime)
