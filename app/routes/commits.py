from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.commit_schema import CommitResponse
from app.services.github_processor import get_all_commits

router = APIRouter(prefix="/commits", tags=["Commits"])

@router.get("", response_model=List[CommitResponse])
def read_commits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Returns stored commits from the database.
    """
    commits = get_all_commits(db, skip=skip, limit=limit)
    return commits
