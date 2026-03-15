from kafka import KafkaConsumer
import json
import logging
import threading
from app.services.github_processor import process_github_push
from app.database import SessionLocal
# Import the engine pipeline for automated analysis
from devhouse_engine.pipeline.pipeline_runner import PipelineRunner

logger = logging.getLogger(__name__)

TOPIC_NAME = 'github-events'

def safe_deserialize(data):
    if not data:
        return None
    try:
        return json.loads(data.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.error(f"[KAFKA CONSUMER] JSON decode error: {e}")
        return None

def consume_events():
    """
    Background worker that listens to Kafka, stores metadata, and triggers AST analysis.
    """
    logger.info(f"[KAFKA CONSUMER] Starting automated pipeline worker for topic: {TOPIC_NAME}")
    
    # Initialize the engine pipeline runner
    pipeline = PipelineRunner()
    
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='github-processor-group',
            value_deserializer=safe_deserialize
        )
        
        for message in consumer:
            payload = message.value
            if payload is None:
                continue
                
            logger.info(f"[KAFKA CONSUMER] Received webhook event. Triggering DB storage...")
            
            # Step 1: Store Commit Metadata in PostgreSQL
            db = SessionLocal()
            try:
                # This populates the commits table
                process_github_push(payload, db)
                logger.info("[KAFKA CONSUMER] Database metadata storage complete.")
                
                # Step 2: Extract details for AST Pipeline trigger
                repository = payload.get("repository", {})
                owner = repository.get("owner", {}).get("name") or repository.get("owner", {}).get("login")
                name = repository.get("name")
                commit_id = payload.get("after") # 'after' is the new HEAD SHA in push events
                ref = payload.get("ref", "refs/heads/main")
                branch = ref.split("/")[-1]

                if owner and name and commit_id:
                    logger.info(f"[KAFKA CONSUMER] Triggering AST Analysis for {owner}/{name} @ {commit_id}")
                    # Run the deep analysis pipeline (AST + Graph)
                    pipeline.process_commit(owner, name, commit_id, branch)
                else:
                    logger.warning("[KAFKA CONSUMER] Could not extract enough metadata for AST trigger.")

            except Exception as e:
                logger.error(f"[KAFKA CONSUMER] Pipeline error: {e}")
            finally:
                db.close()
                
    except Exception as e:
        logger.error(f"[KAFKA CONSUMER] Fatal error in consumer loop: {e}")

def start_kafka_consumer():
    consumer_thread = threading.Thread(target=consume_events, daemon=True)
    consumer_thread.start()
    logger.info("[KAFKA CONSUMER] Background worker thread started.")
