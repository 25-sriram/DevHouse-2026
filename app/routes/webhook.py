# from fastapi import APIRouter, Depends, Request, HTTPException, Header
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.services.commit_service import process_github_push
# import json

# router = APIRouter(prefix="/webhook", tags=["Webhook"])

# @router.post("/github")
# async def github_webhook(
#     request: Request,
#     x_github_event: str = Header(None),
#     db: Session = Depends(get_db)
# ):
#     if x_github_event != "push":
#         return {"status": "ignored", "message": f"Event {x_github_event} ignored"}
        
#     try:
#         payload = await request.json()
#     except json.JSONDecodeError:
#         raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
#     processed_count = process_github_push(payload, db)
#     return {"status": "success", "processed_commits": processed_count}
from fastapi import APIRouter, Header, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.github_processor import process_github_push
from typing import Optional, Dict, Any

router = APIRouter()

@router.post("/webhook/github")
async def github_webhook(
    payload: Dict[str, Any] = Body(default={}),
    x_github_event: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):

    print("Event:", x_github_event)
    print("Payload:", payload)

    if x_github_event == "push":
        processed_count = process_github_push(payload, db)
        return {"status": "received", "processed_commits": processed_count}

    return {"status": "ignored", "message": f"Event {x_github_event} ignored"}
