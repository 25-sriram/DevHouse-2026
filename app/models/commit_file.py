from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class CommitFile(Base):
    __tablename__ = "commit_files"

    commit_id = Column(String, ForeignKey("commits.commit_id"), primary_key=True, index=True)
    file_path = Column(String, primary_key=True)
    file_extension = Column(String)
    change_type = Column(String)  # added / modified / removed
    additions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    language = Column(String)
    patch = Column(String)
    module = Column(String)
    directory = Column(String)
