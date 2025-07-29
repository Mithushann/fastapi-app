import requests
from sqlalchemy.orm import Session
from app.models.github_models import GitHubContributor, GitHubPullRequest
from app.database.db import SessionLocal
from datetime import datetime
from dateutil import parser as dateparser  # pip install python-dateutil

GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/{whatever}"

###Functions to fetch and save GitHub contributors

def fetch_contributors(owner: str, repo: str):
    url = GITHUB_API_URL.format(owner=owner, repo=repo, whatever="contributors")
    response = requests.get(url)
    response.raise_for_status()
    print(f"Fetched {len(response.json())} contributors from {url}👈")
    return response.json()

def save_contributors(db: Session, contributors_data, owner: str, repo: str):
    print(f"Saving {len(contributors_data)} contributors to the database...")
    for contrib in contributors_data:
        # Assuming your model has these fields, adjust as needed
        contributor = GitHubContributor(
            login=contrib.get("login"),
            contributions=contrib.get("contributions"),
            github_user_id=contrib.get("id"),
            avatar_url=contrib.get("avatar_url"),
            html_url=contrib.get("html_url"),
            repo_owner=owner,  # Fallback to owner if not present
            repo_name=repo
        )
        existing = db.query(GitHubContributor).filter(GitHubContributor.github_user_id == contributor.github_user_id).first()

        if existing:
            # Uppdatera fälten om du vill
            existing.contributions = contributor.contributions
        else:
            new_contributor = GitHubContributor(
            login=contributor.login,
            github_user_id=contributor.github_user_id,
            avatar_url=contributor.avatar_url,
            html_url=contributor.html_url,
            contributions=contributor.contributions,
            repo_owner=owner,
            repo_name=repo
            )
            
            db.add(new_contributor)

    db.commit()

def fetch_contributors_and_save(owner: str, repo: str):
    # Create a new DB session
    print("Fetching contributors for...")
    db = SessionLocal()
    try:
        contributors_data = fetch_contributors(owner, repo)
        save_contributors(db, contributors_data, owner, repo)
    except Exception as e:
        print(f"Error fetching or saving contributors: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        
###---------------------------------------------------------------------
### Functions to fetch and save GitHub pull requests

def fetch_pull_requests(owner: str, repo: str):
    url = GITHUB_API_URL.format(owner=owner, repo=repo, whatever="pulls")
    response = requests.get(url)
    response.raise_for_status()
    print(f"Fetched {len(response.json())} pull requests from {url}👈")
    return response.json()

def save_pull_requests(db: Session, pull_requests_data, owner: str, repo: str):
    print(f"Saving {len(pull_requests_data)} pull requests to the database...")
    for pr in pull_requests_data:
        # Assuming your model has these fields, adjust as needed
        pull_request = GitHubPullRequest(
                pr_number = pr.get("number"),
                title = pr.get("title"),
                body = pr.get("body"),
                user_login = pr.get("user", {}).get("login"),
                state = pr.get("state"),
                merged = pr.get("merged"),
                draft = pr.get("draft"),
                repo_owner = owner,
                repo_name = repo
            )
        existing = db.query(GitHubPullRequest).filter(GitHubPullRequest.pr_number == pull_request.pr_number).first()

        if existing:
            # Update fields if you want
            existing.state = pull_request.state
            existing.merged = pull_request.merged
        else:
            new_pull_request = GitHubPullRequest(
                pr_number = pull_request.pr_number,
                title = pull_request.title,
                body = pull_request.body,
                user_login = pull_request.user_login,
                state = pull_request.state,
                merged = pull_request.merged,
                draft = pull_request.draft,
                repo_owner = owner,
                repo_name = repo
            )
            
            db.add(new_pull_request)

    db.commit()
    
def fetch_pull_requests_and_save(owner: str, repo: str):
    print("Fetching pull requests for...")
    db = SessionLocal()
    try:
        pull_requests_data = fetch_pull_requests(owner, repo)
        save_pull_requests(db, pull_requests_data, owner, repo)
    except Exception as e:
        print(f"Error fetching or saving pull requests: {e}")
        db.rollback()
        raise
    finally:
        db.close()