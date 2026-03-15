from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def store_commit(commit_data: dict):
    """
    Helper function to store commit data into PostgreSQL.
    Strictly following the prompt request for a dedicated store_commit function.
    """
    from app.services.github_processor import process_github_push
    db = SessionLocal()
    try:
        processed_count = process_github_push(commit_data, db)
        return processed_count
    except Exception as e:
        print(f"Error in store_commit: {e}")
        raise e
    finally:
        db.close()
