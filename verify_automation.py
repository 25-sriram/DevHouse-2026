from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# This simulates a push to 25-sriram/Dummy_repo
# It uses a real SHA that already exists in your repo
mock_payload = {
    "ref": "refs/heads/main",
    "after": "ba9875c4232bea98b9c6452934e8c28e80985a7c",
    "repository": {
        "name": "Dummy_repo",
        "full_name": "25-sriram/Dummy_repo",
        "html_url": "https://github.com/25-sriram/Dummy_repo",
        "owner": {"login": "25-sriram"},
        "default_branch": "main"
    }
}

producer.send('github-events', mock_payload)
producer.flush()
print("🚀 Simulation event sent! Check your terminal logs for analysis progress.")
