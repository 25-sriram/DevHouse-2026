from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.commit_schema import AnalyticsCommitResponse
from app.services.github_processor import get_all_commits

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/commit-metadata", response_model=List[AnalyticsCommitResponse])
def get_commit_metadata(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Returns normalized commit metadata for analytics dashboard.
    """
    commits = get_all_commits(db, skip=skip, limit=limit)
    return commits
