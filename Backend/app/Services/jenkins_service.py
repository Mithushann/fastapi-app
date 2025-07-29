# app/services/jenkins_service.py
import requests
from sqlalchemy.orm import Session
from app.models.jenkins_models import JenkinsBuild
from app.database.db import SessionLocal
from datetime import datetime
from requests.auth import HTTPBasicAuth
import os

# Base Jenkins URL and credentials from environment variables
JENKINS_BASE_URL = os.getenv("JENKINS_BASE_URL", "https://c902-81-170-208-44.ngrok-free.app")
JENKINS_USER = os.getenv("JENKINS_USER")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN")

def fetch_jenkins_builds(job_name: str):
    url = (
        f"{JENKINS_BASE_URL}/job/{job_name}/api/json"
        f"?tree=builds[number,result,duration,timestamp]"
    )
    auth = HTTPBasicAuth(JENKINS_USER, JENKINS_TOKEN)

    response = requests.get(url, auth=auth)
    response.raise_for_status()

    builds = response.json().get("builds", [])
    detailed_builds = []

    for build in builds:
        detailed_builds.append({
            "number": build.get("number"),
            "result": build.get("result"),
            "duration": (build.get("duration") or 0) / 1000,  # ms to sec
            "timestamp": datetime.fromtimestamp(build.get("timestamp") / 1000)
                if build.get("timestamp") else None,
        })

    print(f"✅ Fetched {len(detailed_builds)} builds with details from {job_name}")
    return detailed_builds


def save_jenkins_builds(db: Session, builds_data, job_name: str):
    print(f"Saving {len(builds_data)} builds to the database...")

    for build in builds_data:
        build_number = build.get("number")
        result = build.get("result")
        duration_sec = build.get("duration")
        timestamp = build.get("timestamp")
        

        existing = db.query(JenkinsBuild).filter(
            JenkinsBuild.job_name == job_name,
            JenkinsBuild.build_number == build_number            
        ).first()

        if existing:
            existing.build_number = build_number
        else:
            new_build = JenkinsBuild(
                job_name=job_name,
                build_number=build_number,
                result=result,
                duration_sec=duration_sec,
                timestamp=timestamp                
            )
            db.add(new_build)

    db.commit()

def fetch_jenkins_builds_and_save(job_name: str):
    db = SessionLocal()
    try:
        builds_data = fetch_jenkins_builds(job_name)
        save_jenkins_builds(db, builds_data, job_name)
    except Exception as e:
        print(f"❌ Error fetching or saving Jenkins builds: {e}")
        db.rollback()
        raise
    finally:
        db.close()
