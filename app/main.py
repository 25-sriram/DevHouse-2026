from fastapi import FastAPI
from app.database import engine, Base
from app.routes import commits, analytics
from app import webhook_router
from app.models import commit, repository
from app.kafka_consumer import start_kafka_consumer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Intelligent Developer Analytics",
    description="A decoupled event-driven backend using FastAPI and Kafka.",
    version="1.1.0"
)

# App Lifecycle
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Developer Analytics System...")
    # Launch Kafka Consumer in the background
    try:
        start_kafka_consumer()
        logger.info("Kafka Consumer integration initialized.")
    except Exception as e:
        logger.error(f"Failed to start Kafka Integration: {e}")

# Routes
app.include_router(analytics.router)
app.include_router(webhook_router.router)
app.include_router(commits.router)

@app.get("/")
def health_check():
    return {"status": "running", "kafka_integration": "active"}
