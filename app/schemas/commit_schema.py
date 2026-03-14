from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CommitBase(BaseModel):
    commit_id: str
    author: str
    message: str
    repository_owner: str
    repository_name: str
    timestamp: datetime
    branch: Optional[str] = None
    additions: Optional[int] = 0
    deletions: Optional[int] = 0
    commit_type: Optional[str] = "general"
    commit_url: Optional[str] = None
    parent_commit_id: Optional[str] = None
    author_email: Optional[str] = None
    commit_category: Optional[str] = None
    commit_message_length: int = 0
    total_changes: Optional[int] = 0
    total_files_in_repo: int = 0
    commit_size: Optional[int] = 0
    is_merge_commit: Optional[bool] = False
    linked_issue: Optional[int] = None
    pull_request_number: Optional[int] = None
    pr_title: Optional[str] = None
    pr_labels: List[str] = []

class CommitFileBase(BaseModel):
    file_path: str
    file_extension: str
    change_type: str
    additions: int = 0
    deletions: int = 0
    language: str
    patch: Optional[str] = None
    module: Optional[str] = None
    directory: Optional[str] = None

class CommitFileCreate(CommitFileBase):
    pass

class CommitFileResponse(CommitFileBase):
    commit_id: str

    class Config:
        from_attributes = True

class CommitCreate(CommitBase):
    pass

class CommitResponse(CommitBase):
    id: int
    files: Optional[List[CommitFileResponse]] = []

    class Config:
        from_attributes = True

class AnalyticsCommitResponse(BaseModel):
    commit_id: str
    author: str
    commit_type: str
    repository_owner: str
    repository_name: str
    commit_message_length: int
    total_files_in_repo: int
    timestamp: datetime

    class Config:
        from_attributes = True
