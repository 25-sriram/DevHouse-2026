from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
import datetime

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    repo_url = Column(String, unique=True, index=True)
    repo_owner = Column(String)
    repo_name = Column(String)
    default_branch = Column(String, default="main")
    last_processed_commit = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
