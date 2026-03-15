import os
from git import Repo, exc
import logging
from devhouse_engine.config.settings import settings

logger = logging.getLogger(__name__)

class RepositoryLoader:
    def __init__(self):
        self.repos_root = settings.REPOS_ROOT
        if not os.path.exists(self.repos_root):
            os.makedirs(self.repos_root)

    def _get_repo_path(self, owner, name):
        return os.path.join(self.repos_root, f"{owner}_{name}")

    def load_repository(self, owner, name, commit_id, branch="main"):
        """
        Ensures the repository is present, updated, and on the correct commit.
        """
        repo_url = f"https://github.com/{owner}/{name}.git"
        repo_path = self._get_repo_path(owner, name)
        
        try:
            if not os.path.exists(repo_path):
                logger.info(f"Cloning {repo_url} to {repo_path}")
                repo = Repo.clone_from(repo_url, repo_path)
            else:
                logger.info(f"Using existing repository at {repo_path}. Fetching updates.")
                repo = Repo(repo_path)
                # Ensure we are not in a detached HEAD that prevents pulling
                try:
                    repo.git.checkout(branch)
                    repo.remotes.origin.pull()
                except exc.GitCommandError as ge:
                    logger.warning(f"Could not pull latest for {branch}: {ge}. Attempting fetch.")
                    repo.remotes.origin.fetch()
            
            logger.info(f"Checking out target commit {commit_id}")
            repo.git.checkout(commit_id)
            return repo_path
        except Exception as e:
            logger.error(f"Failed to load/update repository {owner}/{name} at {commit_id}: {e}")
            return None

    def get_modified_files(self, owner, name, commit_id):
        repo_path = self._get_repo_path(owner, name)
        if not os.path.exists(repo_path):
            return []
            
        try:
            repo = Repo(repo_path)
            commit = repo.commit(commit_id)
            
            if commit.parents:
                diff = commit.parents[0].diff(commit)
            else:
                from git import NULL_TREE
                diff = commit.diff(NULL_TREE, reverse=True)
                
            modified_files = []
            for d in diff:
                path = d.b_path if d.b_path else d.a_path
                if path and path.endswith('.py'):
                    modified_files.append(path)
            return list(set(modified_files))
        except Exception as e:
            logger.error(f"Failed to get modified files for {commit_id}: {e}")
            return []
