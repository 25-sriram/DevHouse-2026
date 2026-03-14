from sqlalchemy.orm import Session
from app.models.commit import Commit
from dateutil.parser import parse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def process_github_push(payload: dict, db: Session) -> int:
    """
    Processes a GitHub webhook push event payload and stores commits in the database.
    Returns the number of new commits stored.
    """
    repository = payload.get("repository", {}).get("full_name", "unknown_repo")
    commits_data = payload.get("commits", [])
    
    new_commits_count = 0
    
    for commit_data in commits_data:
        commit_id = commit_data.get("id")
        author = commit_data.get("author", {}).get("name", "Unknown Author")
        message = commit_data.get("message", "")
        timestamp_str = commit_data.get("timestamp")
        
        timestamp = datetime.utcnow()
        if timestamp_str:
            try:
                timestamp = parse(timestamp_str).replace(tzinfo=None)
            except Exception:
                logger.warning(f"Could not parse timestamp: {timestamp_str}")
                
        existing = db.query(Commit).filter(Commit.commit_id == commit_id).first()
        if existing:
            continue
            
        new_commit = Commit(
            commit_id=commit_id,
            author=author,
            message=message,
            repository=repository,
            timestamp=timestamp
        )
        db.add(new_commit)
        new_commits_count += 1
        
    db.commit()
    return new_commits_count

def get_all_commits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Commit).offset(skip).limit(limit).all()
