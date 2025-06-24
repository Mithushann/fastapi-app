# app/services/jenkins_service.py
import requests
from sqlalchemy.orm import Session
from app.models.jenkins_models import JenkinsBuild
from app.database.db import SessionLocal
from datetime import datetime
from requests.auth import HTTPBasicAuth

# Replace these with your Jenkins credentials and base URL
JENKINS_URL = "http://your-jenkins-url"
JENKINS_USER = "your-username"
JENKINS_API_TOKEN = "your-token"

def fetch_jenkins_builds(job_name: str):
    url = f"{JENKINS_URL}/job/{job_name}/api/json?tree=builds[number,result,duration,timestamp]"
    auth = HTTPBasicAuth(JENKINS_USER, JENKINS_API_TOKEN)
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    builds = response.json().get("builds", [])
    print(f"✅ Fetched {len(builds)} builds from {job_name}")
    return builds

def save_jenkins_builds(db: Session, builds_data, job_name: str):
    print(f"Saving {len(builds_data)} builds to the database...")

    for build in builds_data:
        build_number = build.get("number")
        result = build.get("result")
        duration_sec = build.get("duration", 0) / 1000  # Jenkins reports in ms
        timestamp = datetime.fromtimestamp(build.get("timestamp", 0) / 1000)

        existing = db.query(JenkinsBuild).filter(
            JenkinsBuild.job_name == job_name,
            JenkinsBuild.build_number == build_number
        ).first()

        if existing:
            existing.result = result
            existing.duration_sec = duration_sec
            existing.timestamp = timestamp
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