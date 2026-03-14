from sqlalchemy.orm import Session
from app.models.commit import Commit
from app.schemas.commit_schema import CommitCreate
from app.services.event_normalizer import normalize_push_event
from app.config import settings
import logging
import requests
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def fetch_commit_stats(repo_full_name: str, commit_sha: str) -> Optional[Dict[str, int]]:
    """Fetches commit statistics from GitHub API."""
    url = f"https://api.github.com/repos/{repo_full_name}/commits/{commit_sha}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if getattr(settings, "github_token", None):
        headers["Authorization"] = f"token {settings.github_token}"
        
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        stats = data.get("stats", {})
        files = data.get("files", [])
        return {
            "additions": stats.get("additions", 0),
            "deletions": stats.get("deletions", 0),
            "files_changed": len(files)
        }
    except Exception as e:
        logger.warning(f"Failed to fetch stats for {commit_sha} in {repo_full_name}: {e}")
        return None

def process_github_push(payload: Dict[str, Any], db: Session) -> int:
    """
    Processes a GitHub webhook push event payload, normalizes the events, 
    and stores new commits in the database.
    Returns the number of new commits stored.
    """
    normalized_commits = normalize_push_event(payload)
    new_commits_count = 0

    for norm_commit in normalized_commits:
        existing = db.query(Commit).filter(Commit.commit_id == norm_commit.commit_id).first()
        if existing:
            continue

        # Fetch enhanced stats from GitHub API
        stats = fetch_commit_stats(norm_commit.repository, norm_commit.commit_id)
        if stats:
            norm_commit.additions = stats["additions"]
            norm_commit.deletions = stats["deletions"]
            norm_commit.files_changed = stats["files_changed"]

        new_commit = Commit(**norm_commit.model_dump())
        db.add(new_commit)
        
        logger.info(f"Saving commit {norm_commit.commit_id[:7]} | additions={norm_commit.additions} | deletions={norm_commit.deletions} | files_changed={norm_commit.files_changed}")
        new_commits_count += 1

    db.commit()
    return new_commits_count

def get_all_commits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Commit).offset(skip).limit(limit).all()
