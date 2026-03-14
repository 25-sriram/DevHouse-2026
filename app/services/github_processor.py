from sqlalchemy.orm import Session
from app.models.commit import Commit
from app.models.commit_file import CommitFile
from app.schemas.commit_schema import CommitCreate, CommitFileCreate
from app.services.event_normalizer import normalize_push_event
from app.config import settings
import logging
import requests
from typing import Dict, Any, Optional, Tuple, List

logger = logging.getLogger(__name__)

def fetch_commit_stats_and_files(repo_full_name: str, commit_sha: str) -> Optional[Tuple[Dict[str, int], List[Dict[str, Any]]]]:
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
            "total": stats.get("total", 0),
            "files_changed": len(files)
        }, files
    except Exception as e:
        logger.warning(f"Failed to fetch stats/files for {commit_sha} in {repo_full_name}: {e}")
        return None, []

def fetch_repo_file_count(repo_full_name: str, commit_sha: str) -> int:
    """Fetch total number of blob files in the repository at a given commit."""
    url = f"https://api.github.com/repos/{repo_full_name}/git/trees/{commit_sha}?recursive=1"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if getattr(settings, "github_token", None):
        headers["Authorization"] = f"token {settings.github_token}"
        
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        tree_elements = data.get("tree", [])
        return sum(1 for item in tree_elements if item.get("type") == "blob")
    except Exception as e:
        logger.warning(f"Failed to fetch tree size for {commit_sha} in {repo_full_name}: {e}")
        return 0

def process_github_push(payload: Dict[str, Any], db: Session) -> int:
    logger.info("Received GitHub webhook push event")
    normalized_commits, commit_files_map = normalize_push_event(payload)
    new_commits_count = 0

    for norm_commit in normalized_commits:
        existing = db.query(Commit).filter(Commit.commit_id == norm_commit.commit_id).first()
        if existing:
            continue
            
        repo_owner_name = f"{norm_commit.repository_owner}/{norm_commit.repository_name}"
        commit_id = norm_commit.commit_id
        
        files_data: List[CommitFileCreate] = commit_files_map.get(commit_id, [])

        api_result = fetch_commit_stats_and_files(repo_owner_name, commit_id)
        if api_result:
            stats, api_files = api_result
            if stats:
                norm_commit.additions = stats["additions"]
                norm_commit.deletions = stats["deletions"]
                norm_commit.total_changes = stats["total"]
                norm_commit.commit_size = stats["total"]
                
            total_files_count = fetch_repo_file_count(repo_owner_name, commit_id)
            norm_commit.total_files_in_repo = total_files_count
                
            api_file_map = {f.get("filename"): f for f in api_files}
            for fd in files_data:
                matching_api_file = api_file_map.get(fd.file_path)
                if matching_api_file:
                    fd.additions = matching_api_file.get("additions", 0)
                    fd.deletions = matching_api_file.get("deletions", 0)
                    fd.patch = matching_api_file.get("patch", None)

        logger.info(f"Processing commit {commit_id[:7]}")
        logger.info(f"Extracted repository owner: {norm_commit.repository_owner}")
        logger.info(f"Extracted repository name: {norm_commit.repository_name}")
        logger.info(f"Computed commit_message_length: {norm_commit.commit_message_length}")
        logger.info(f"Dynamically mapped total repository files: {norm_commit.total_files_in_repo}")
        logger.info(f"Extracted {len(files_data)} changed files")
        
        if len(files_data) > 0:
            logger.info(f"Extracted module: {files_data[0].module}")
            logger.info(f"Extracted directory: {files_data[0].directory}")

        new_commit = Commit(**norm_commit.model_dump())
        db.add(new_commit)
        db.flush()
        
        for file_data in files_data:
            db_file = CommitFile(commit_id=commit_id, **file_data.model_dump())
            db.add(db_file)
            
        logger.info("Stored commit and file metadata successfully")
        new_commits_count += 1

    db.commit()
    return new_commits_count

def get_all_commits(db: Session, skip: int = 0, limit: int = 100):
    commits = db.query(Commit).offset(skip).limit(limit).all()
    for commit in commits:
        files = db.query(CommitFile).filter(CommitFile.commit_id == commit.commit_id).all()
        commit.files = files
    return commits
