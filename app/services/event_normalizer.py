from typing import List, Dict, Any
from app.schemas.commit_schema import CommitCreate
from dateutil.parser import parse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def classify_commit(message: str) -> str:
    """Classify the commit based on its message prefix."""
    message_lower = message.lower().strip()
    if message_lower.startswith("feat"):
        return "feature"
    elif message_lower.startswith("fix"):
        return "bugfix"
    elif message_lower.startswith("refactor"):
        return "architecture"
    elif message_lower.startswith("docs"):
        return "documentation"
    elif message_lower.startswith("test"):
        return "testing"
    else:
        return "general"

def normalize_push_event(payload: Dict[str, Any]) -> List[CommitCreate]:
    """
    Transforms raw GitHub webhook push payloads into normalized commit metadata.
    """
    repository = payload.get("repository", {}).get("full_name", "unknown_repo")
    
    # Extract branch from ref (e.g., 'refs/heads/main' -> 'main')
    ref = payload.get("ref", "")
    branch = ref.split("/")[-1] if "/" in ref else ref

    commits_data = payload.get("commits", [])
    normalized_commits = []

    for commit in commits_data:
        commit_id = commit.get("id")
        author = commit.get("author", {}).get("name", "Unknown Author")
        message = commit.get("message", "")
        commit_url = commit.get("url", "")
        timestamp_str = commit.get("timestamp")

        # Parse timestamp safely
        timestamp = datetime.utcnow()
        if timestamp_str:
            try:
                timestamp = parse(timestamp_str).replace(tzinfo=None)
            except Exception:
                logger.warning(f"Could not parse timestamp: {timestamp_str}")

        # Extract file change metrics
        added = commit.get("added", [])
        removed = commit.get("removed", [])
        modified = commit.get("modified", [])
        files_changed = len(added) + len(removed) + len(modified)

        # Classify commit type
        commit_type = classify_commit(message)

        # Default fallback values for stats (overridden by github_processor API fetch if successful)
        additions = 0
        deletions = 0

        normalized = CommitCreate(
            commit_id=commit_id,
            author=author,
            message=message,
            repository=repository,
            timestamp=timestamp,
            branch=branch,
            files_changed=files_changed,
            additions=additions,
            deletions=deletions,
            commit_type=commit_type,
            commit_url=commit_url
        )
        normalized_commits.append(normalized)

    return normalized_commits
