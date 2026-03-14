from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class Commit(Base):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, index=True)
    commit_id = Column(String, unique=True, index=True)
    author = Column(String, index=True)
    message = Column(String)
    repository = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    branch = Column(String, index=True)
    files_changed = Column(Integer, default=0)
    additions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    commit_type = Column(String, index=True)
    commit_url = Column(String)
