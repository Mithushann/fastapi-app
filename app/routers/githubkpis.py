from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.github_models import GitHubContributor, GitHubPullRequest
from app.database.dependencies import get_db

router = APIRouter()

@router.get("/contributors")
def get_contributors(owner: str, repo: str, db: Session = Depends(get_db)):
    try:
        contributors = db.query(GitHubContributor).filter_by(repo_owner=owner, repo_name=repo).all()
        return contributors
    finally:
        db.close()
        
@router.get("/pullrequests")
def get_pull_requests(owner: str, repo: str, db: Session = Depends(get_db)):
    try:
        pull_requests = db.query(GitHubPullRequest).filter_by(repo_owner=owner, repo_name=repo).all()
        return pull_requests
    finally:
        db.close()