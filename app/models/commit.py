from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from app.database import Base
from datetime import datetime

class Commit(Base):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, index=True)
    commit_id = Column(String, unique=True, index=True)
    author = Column(String, index=True)
    message = Column(String)
    repository_owner = Column(String, index=True)
    repository_name = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    branch = Column(String, index=True)
    additions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    commit_type = Column(String, index=True)
    commit_url = Column(String)
    parent_commit_id = Column(String)
    author_email = Column(String)
    commit_category = Column(String)
    commit_message_length = Column(Integer)
    total_changes = Column(Integer, default=0)
    total_files_in_repo = Column(Integer, default=0)
    commit_size = Column(Integer, default=0)
    is_merge_commit = Column(Boolean, default=False)
    linked_issue = Column(Integer, nullable=True)
    pull_request_number = Column(Integer, nullable=True)
    pr_title = Column(String, nullable=True)
    pr_labels = Column(JSON, default=list, nullable=False)
