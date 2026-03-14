from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.commit_schema import CommitResponse, AnalyticsCommitResponse
from app.services.github_processor import get_all_commits
from app.models.commit import Commit
from app.models.commit_file import CommitFile

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/commit-metadata", response_model=List[AnalyticsCommitResponse])
def get_commit_metadata(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Returns normalized commit metadata for analytics dashboard.
    """
    commits = get_all_commits(db, skip=skip, limit=limit)
    return commits

@router.get("/commit-details", response_model=List[CommitResponse])
def get_commit_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Returns full detailed metadata, including module mapping, 
    language detection, issue references and file-level patch arrays.
    """
    commits = get_all_commits(db, skip=skip, limit=limit)
    return commits
