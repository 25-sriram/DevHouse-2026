from pydantic import BaseModel
from datetime import datetime

class CommitBase(BaseModel):
    commit_id: str
    author: str
    message: str
    repository: str
    timestamp: datetime

class CommitCreate(CommitBase):
    pass

class CommitResponse(CommitBase):
    id: int

    class Config:
        from_attributes = True
