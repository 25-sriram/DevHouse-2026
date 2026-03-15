import psycopg2
from psycopg2.extras import Json
import logging
from devhouse_engine.config.settings import settings

logger = logging.getLogger(__name__)

class PostgresClient:
    def __init__(self):
        self.conn_params = {
            "dbname": settings.POSTGRES_DB,
            "user": settings.POSTGRES_USER,
            "password": settings.POSTGRES_PASSWORD,
            "host": settings.POSTGRES_HOST,
            "port": settings.POSTGRES_PORT
        }
        self._setup_db()

    def _get_connection(self):
        return psycopg2.connect(**self.conn_params)

    def _setup_db(self):
        """Create the code_structure table if it doesn't exist."""
        query = """
        CREATE TABLE IF NOT EXISTS code_structure (
            id SERIAL PRIMARY KEY,
            commit_id VARCHAR(255) NOT NULL,
            file_name TEXT NOT NULL,
            classes JSONB DEFAULT '[]',
            functions JSONB DEFAULT '[]',
            imports JSONB DEFAULT '[]',
            calls JSONB DEFAULT '[]',
            UNIQUE(commit_id, file_name)
        );
        """
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(query)
            conn.commit()
            logger.info("code_structure table initialized.")
        except Exception as e:
            logger.error(f"Failed to setup database: {e}")
            conn.rollback()
        finally:
            conn.close()

    def fetch_commits_to_analyze(self, limit=10):
        """Fetch commits that haven't been analyzed yet."""
        # For now, we fetch all commits from the commits table.
        # In a real system, we'd have a status column.
        query = "SELECT commit_id, repository_owner, repository_name, branch FROM commits LIMIT %s;"
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(query, (limit,))
                return cur.fetchall()
        except Exception as e:
            logger.error(f"Failed to fetch commits: {e}")
            return []
        finally:
            conn.close()

    def store_code_structure(self, commit_id, file_name, structure):
        """Store parsed AST data in JSONB format."""
        query = """
        INSERT INTO code_structure (commit_id, file_name, classes, functions, imports, calls)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (commit_id, file_name) 
        DO UPDATE SET 
            classes = EXCLUDED.classes,
            functions = EXCLUDED.functions,
            imports = EXCLUDED.imports,
            calls = EXCLUDED.calls;
        """
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(query, (
                    commit_id, 
                    file_name, 
                    Json(structure.get("classes", [])),
                    Json(structure.get("functions", [])),
                    Json(structure.get("imports", [])),
                    Json(structure.get("calls", []))
                ))
            conn.commit()
            logger.info(f"Stored structure for {file_name} in {commit_id}")
        except Exception as e:
            logger.error(f"Failed to store code structure: {e}")
            conn.rollback()
        finally:
            conn.close()
