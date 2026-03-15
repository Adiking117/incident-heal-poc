from fastapi import FastAPI, Request
from kafka import KafkaProducer
import json

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

@app.post("/alert")
async def receive_alert(request: Request):

    data = await request.json()

    print("Alert received:")
    print(data)

    producer.send("incidents", data)

    return {"status": "sent to kafka"}