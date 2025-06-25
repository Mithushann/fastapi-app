# app/main.py
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from app.routers import example, githubkpis
from app.database.db import SessionLocal, engine
from app.models import github_models
from app.utils.fetch_github import fetch_contributors_and_save, fetch_pull_requests_and_save  # assumed to be SYNC

from datetime import datetime
import pytz

def start_scheduler():
    scheduler = BackgroundScheduler()

    def job():
        try:
            tz = pytz.timezone("Europe/Stockholm")  # or your desired timezone
            now_local = datetime.now(tz)
            print(f"🔁 Running fetch job at {now_local.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            fetch_contributors_and_save("menloresearch", "jan")  # sync function!
            fetch_pull_requests_and_save("menloresearch", "jan")  # sync function!
        except Exception as e:
            print("❌ Error in scheduler job:", e)

    scheduler.add_job(job, trigger="interval", minutes=5 ) ### how often to run the job?
    scheduler.start()
    return scheduler

print("⏳ Creating database tables...")
github_models.Base.metadata.create_all(bind=engine)

print("🚀 Initializing FastAPI app...")
app = FastAPI()

print("📂 Registering routers...")
app.include_router(example.router)
app.include_router(githubkpis.router)

print("⏰ Starting scheduler...")
scheduler = start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    print("🛑 Shutting down scheduler...")
    scheduler.shutdown()