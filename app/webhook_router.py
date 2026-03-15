from fastapi import APIRouter, Header, Body, HTTPException
from app.kafka_producer import send_commit_event
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/webhook/github")
async def github_webhook(
    payload: Dict[str, Any] = Body(default={}),
    x_github_event: Optional[str] = Header(None)
):
    """
    Asynchronous Webhook Ingestion:
    Receives GitHub events and publishes them to Kafka for background processing.
    """
    logger.info(f"Received GitHub event: {x_github_event}")

    if x_github_event == "push":
        try:
            # Send the event to Kafka instead of processing directly
            send_commit_event(payload)
            return {
                "status": "accepted", 
                "message": "Event published to Kafka for background processing"
            }
        except Exception as e:
            logger.error(f"Failed to publish event to Kafka: {e}")
            raise HTTPException(status_code=500, detail="Internal event streaming error")

    return {"status": "ignored", "message": f"Event {x_github_event} ignored"}
