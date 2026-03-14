from typing import List, Dict, Any, Tuple, Optional
from app.schemas.commit_schema import CommitCreate, CommitFileCreate
from dateutil.parser import parse
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)

# Basic language mapping
EXTENSION_MAPPING = {
    "py": "python",
    "js": "javascript",
    "ts": "typescript",
    "java": "java",
    "go": "go",
    "rb": "ruby",
    "cpp": "c++",
    "c": "c",
    "html": "html",
    "css": "css",
    "md": "markdown",
    "json": "json"
}

def classify_commit(message: str) -> str:
    message_lower = message.lower().strip()
    if message_lower.startswith("feat"): return "feature"
    elif message_lower.startswith("fix"): return "bugfix"
    elif message_lower.startswith("refactor"): return "architecture"
    elif message_lower.startswith("docs"): return "documentation"
    elif message_lower.startswith("test"): return "testing"
    return "general"

def is_merge_commit(message: str) -> bool:
    message_lower = message.lower()
    return "merge branch" in message_lower or "merge pull request" in message_lower

def extract_issue_and_pr(message: str) -> Tuple[Optional[int], Optional[int]]:
    """Extracts linked issues (#123, Fix #123, JIRA-123) and PRs."""
    linked_issue = None
    pr_id = None
    
    issue_match = re.search(r'(?:#|JIRA-)(\d+)', message, flags=re.IGNORECASE)
    if issue_match:
        linked_issue = int(issue_match.group(1))
        
    pr_match = re.search(r'Merge pull request #(\d+)', message, flags=re.IGNORECASE)
    if pr_match:
        pr_id = int(pr_match.group(1))
        
    return linked_issue, pr_id

def extract_file_metadata(file_path: str) -> Tuple[str, str, str, str]:
    """Returns: file_extension, language, module, directory"""
    parts = file_path.split("/")
    file_name = parts[-1]
    
    ext_parts = file_name.split(".")
    file_extension = ext_parts[-1].lower() if len(ext_parts) > 1 else ""
    
    language = EXTENSION_MAPPING.get(file_extension, "unknown")
    
    if len(parts) == 1:
        directory = "root"
        module = "root"
    else:
        directory = "/".join(parts[:-1])
        dirs = parts[:-1]
        
        module = dirs[0]
        if "src" in dirs:
            src_index = dirs.index("src")
            if src_index + 1 < len(dirs):
                module = dirs[src_index + 1]
            else:
                module = dirs[src_index]
                
    return file_extension, language, module, directory

def normalize_push_event(payload: Dict[str, Any]) -> Tuple[List[CommitCreate], Dict[str, List[CommitFileCreate]]]:
    repository_full_name = payload.get("repository", {}).get("full_name", "unknown/unknown")
    owner_name_parts = repository_full_name.split("/")
    repository_owner = owner_name_parts[0] if len(owner_name_parts) > 0 else "unknown"
    repository_name = owner_name_parts[1] if len(owner_name_parts) > 1 else "unknown"
    
    ref = payload.get("ref", "")
    branch = ref.split("/")[-1] if "/" in ref else ref

    commits_data = payload.get("commits", [])
    
    normalized_commits = []
    commit_files_map = {}

    for commit in commits_data:
        commit_id = commit.get("id")
        author_name = commit.get("author", {}).get("name", "Unknown Author")
        author_email = commit.get("author", {}).get("email", None)
        message = commit.get("message", "")
        commit_url = commit.get("url", "")
        timestamp_str = commit.get("timestamp")

        timestamp = datetime.utcnow()
        if timestamp_str:
            try:
                timestamp = parse(timestamp_str).replace(tzinfo=None)
            except Exception:
                logger.warning(f"Could not parse timestamp: {timestamp_str}")

        commit_type = classify_commit(message)
        merge_flag = is_merge_commit(message)
        linked_issue, _ = extract_issue_and_pr(message)
        
        parent_commit_id = commit.get("parent")
        if not parent_commit_id and len(normalized_commits) > 0:
            parent_commit_id = normalized_commits[-1].commit_id

        commit_files = []
        
        for file_path in commit.get("added", []):
            f_ext, lang, mod, d = extract_file_metadata(file_path)
            commit_files.append(CommitFileCreate(
                file_path=file_path, file_extension=f_ext,
                change_type="added", language=lang, module=mod, directory=d
            ))
            
        for file_path in commit.get("removed", []):
            f_ext, lang, mod, d = extract_file_metadata(file_path)
            commit_files.append(CommitFileCreate(
                file_path=file_path, file_extension=f_ext,
                change_type="removed", language=lang, module=mod, directory=d
            ))
            
        for file_path in commit.get("modified", []):
            f_ext, lang, mod, d = extract_file_metadata(file_path)
            commit_files.append(CommitFileCreate(
                file_path=file_path, file_extension=f_ext,
                change_type="modified", language=lang, module=mod, directory=d
            ))

        normalized_commit = CommitCreate(
            commit_id=commit_id,
            author=author_name,
            author_email=author_email,
            message=message,
            repository_owner=repository_owner,
            repository_name=repository_name,
            timestamp=timestamp,
            branch=branch,
            additions=0,
            deletions=0,
            total_changes=0,
            total_files_in_repo=0,
            commit_size=0,
            commit_type=commit_type,
            commit_category=commit_type,
            commit_message_length=len(message) if message else 0,
            commit_url=commit_url,
            is_merge_commit=merge_flag,
            linked_issue=linked_issue,
            pull_request_number=None,
            pr_title=None,
            pr_labels=[],
            parent_commit_id=parent_commit_id
        )
        
        normalized_commits.append(normalized_commit)
        commit_files_map[commit_id] = commit_files

    return normalized_commits, commit_files_map
