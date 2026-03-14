from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommitBase(BaseModel):
    commit_id: str
    author: str
    message: str
    repository: str
    timestamp: datetime
    branch: Optional[str] = None
    files_changed: Optional[int] = 0
    additions: Optional[int] = 0
    deletions: Optional[int] = 0
    commit_type: Optional[str] = "general"
    commit_url: Optional[str] = None

class CommitCreate(CommitBase):
    pass

class CommitResponse(CommitBase):
    id: int

    class Config:
        from_attributes = True

class AnalyticsCommitResponse(BaseModel):
    commit_id: str
    author: str
    commit_type: str
    files_changed: int
    repository: str
    timestamp: datetime

    class Config:
        from_attributes = True
