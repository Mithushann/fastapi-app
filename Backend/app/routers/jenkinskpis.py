from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.models.jenkins_models import JenkinsBuild

router = APIRouter()

@router.get("/builds")
def get_builds(job_name: str, db: Session = Depends(get_db)):
    builds = db.query(JenkinsBuild).filter_by(job_name=job_name).all()
    if not builds:
        raise HTTPException(status_code=404, detail="No builds found for this job")
    return builds