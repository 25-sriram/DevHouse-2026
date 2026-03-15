from kafka import KafkaConsumer
import json
import logging
import threading
from app.services.github_processor import process_github_push
from app.database import SessionLocal

logger = logging.getLogger(__name__)

TOPIC_NAME = 'github-events'

def safe_deserialize(data):
    """
    Safely deserialize JSON data. Returns None if decoding fails.
    """
    if not data:
        return None
    try:
        return json.loads(data.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.error(f"[KAFKA CONSUMER] JSON decode error: {e}. Message data: {data}")
        return None

def consume_events():
    """
    Background worker that listens to Kafka and stores commits in PostgreSQL.
    """
    logger.info(f"[KAFKA CONSUMER] Starting consumer for topic: {TOPIC_NAME}")
    
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
            
            # Skip empty or malformed payloads
            if payload is None:
                continue
                
            logger.info(f"[KAFKA CONSUMER] Received event from Kafka")
            
            # Create a new database session for each processing task
            db = SessionLocal()
            try:
                # Reuse the existing robust processing logic
                process_github_push(payload, db)
                logger.info("[KAFKA CONSUMER] Successfully processed and stored commit data")
            except Exception as e:
                logger.error(f"[KAFKA CONSUMER] Error storing commit: {e}")
            finally:
                db.close()
                
    except Exception as e:
        logger.error(f"[KAFKA CONSUMER] Fatal error in consumer loop: {e}")

def start_kafka_consumer():
    """
    Starts the Kafka consumer in a separate background thread.
    """
    consumer_thread = threading.Thread(target=consume_events, daemon=True)
    consumer_thread.start()
    logger.info("[KAFKA CONSUMER] Background thread started")
