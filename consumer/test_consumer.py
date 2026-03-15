from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "incidents",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("🚀 Incident consumer started...")

for message in consumer:
    print("\n🔥 INCIDENT EVENT RECEIVED")
    print("Topic:", message.topic)
    print("Partition:", message.partition)
    print("Offset:", message.offset)
    print("Payload:", message.value)