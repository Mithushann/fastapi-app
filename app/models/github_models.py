# models/github_models.py
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from app.database.db import Base

class GitHubContributor(Base):
    __tablename__ = "githubcontributor"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, nullable=False)
    github_user_id = Column(Integer, unique=True, nullable=False)
    avatar_url = Column(String)
    html_url = Column(String)
    contributions = Column(Integer)
    repo_owner = Column(String, nullable=False) 
    repo_name = Column(String, nullable=False)
    
class GitHubCommit(Base):
    __tablename__ = "githubcommits"
    sha = Column(String, primary_key=True)
    repo = Column(String)
    author_login = Column(String)
    committed_date = Column(DateTime)

class GitHubPullRequest(Base):
    __tablename__ = "github_pullrequests"

    id = Column(Integer, primary_key=True, index=True)
    pr_number = Column(Integer, nullable=False, index=True)
    repo_owner = Column(String, nullable=False, index=True)
    repo_name = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    body = Column(String)
    user_login = Column(String, nullable=False, index=True)
    state = Column(String, nullable=False)  # e.g. 'open', 'closed', 'merged'
    merged = Column(Boolean, default=False)
    draft = Column(Boolean, default=False)