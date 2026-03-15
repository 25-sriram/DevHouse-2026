import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # PostgreSQL Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/developer_analytics")
    
    # Parse individual components for clients that need them (like psycopg2 connection params)
    # This ensures "postgres" isn't used as a fallback if DATABASE_URL is set in .env
    import urllib.parse as urlparse
    _url = urlparse.urlparse(DATABASE_URL)
    
    POSTGRES_DB = _url.path[1:]
    POSTGRES_USER = _url.username
    POSTGRES_PASSWORD = _url.password
    POSTGRES_HOST = _url.hostname
    POSTGRES_PORT = _url.port
    
    # Neo4j Configuration
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "devhouse")
    
    # Repository Configuration
    REPOS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "repos"))
    
settings = Settings()
