from fastapi import FastAPI
from app.database import engine, Base
from app.routes import webhook, commits, analytics
from app.models import commit  # Import models to ensure they are registered

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Developer Analytics System",
    description="A modular FastAPI backend that integrates with GitHub webhooks for developer analytics.",
    version="1.0.0"
)

# Future modules configuration
app.include_router(analytics.router)
# app.include_router(ai_insights.router)

app.include_router(webhook.router)
app.include_router(commits.router)

@app.get("/")
def health_check():
    return {"status": "running"}
