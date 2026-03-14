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
