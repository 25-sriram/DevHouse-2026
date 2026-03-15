from kafka import KafkaProducer
import json
import logging

logger = logging.getLogger(__name__)

# Configure Kafka Producer
# Integration note: Ensure Kafka is running on localhost:9092
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',
    retries=3
)

TOPIC_NAME = 'github-events'

def send_commit_event(payload: dict):
    """
    Sends the GitHub webhook payload to the Kafka topic.
    """
    try:
        logger.info(f"[KAFKA PRODUCER] Sending event to topic: {TOPIC_NAME}")
        producer.send(TOPIC_NAME, payload)
        producer.flush()
        logger.info("[KAFKA PRODUCER] Event sent successfully")
    except Exception as e:
        logger.error(f"[KAFKA PRODUCER] Failed to send event: {e}")
        # In a real production system, you might want to implement a fallback 
        # storage or retry mechanism here.
        raise e
