import logging
import sys
import os

# Ensure devhouse_engine is in path if run as a script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from devhouse_engine.database.postgres_client import PostgresClient
from devhouse_engine.parser.repository_loader import RepositoryLoader
from devhouse_engine.parser.ast_parser import ASTParser
from devhouse_engine.graph.neo4j_connector import Neo4jConnector
from devhouse_engine.graph.graph_builder import GraphBuilder

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PipelineRunner:
    def __init__(self):
        self.pg_client = PostgresClient()
        self.repo_loader = RepositoryLoader()
        self.neo4j_conn = Neo4jConnector()
        self.graph_builder = GraphBuilder(self.neo4j_conn)

    def process_commit(self, owner, name, commit_id, branch="main"):
        """
        Processes a single commit: updates repo, parses AST, and builds graph.
        This is the main entry point for automated triggers.
        """
        logger.info(f"[PIPELINE] Starting analysis for {owner}/{name} @ {commit_id} on {branch}")
        
        try:
            # 1. Load/Update Repository
            repo_path = self.repo_loader.load_repository(owner, name, commit_id, branch)
            if not repo_path:
                logger.error(f"[PIPELINE] Failed to load repository {owner}/{name}")
                return False

            # 2. Identify modified Python files
            modified_files = self.repo_loader.get_modified_files(owner, name, commit_id)
            logger.info(f"[PIPELINE] Found {len(modified_files)} Python files to analyze.")

            for rel_path in modified_files:
                full_path = os.path.join(repo_path, rel_path)
                logger.debug(f"[PIPELINE] Parsing AST for {rel_path}")
                
                # 3. AST Parse
                structure = ASTParser.parse_file(full_path)
                if structure:
                    # 4. Store in PostgreSQL
                    self.pg_client.store_code_structure(commit_id, rel_path, structure)
                    
                    # 5. Build Graph in Neo4j
                    self.graph_builder.build_file_dependency(commit_id, rel_path, structure)
            
            logger.info(f"[PIPELINE] Successfully completed analysis for commit {commit_id}")
            return True
            
        except Exception as e:
            logger.error(f"[PIPELINE] Error during commit processing: {e}")
            return False

    def run_batch(self, limit=10):
        """
        Batch process pending commits from the database.
        (Legacy/Fallback mode)
        """
        commits = self.pg_client.fetch_commits_to_analyze(limit=limit)
        for commit_id, owner, name, branch in commits:
            self.process_commit(owner, name, commit_id, branch)

if __name__ == "__main__":
    runner = PipelineRunner()
    runner.run_batch()
