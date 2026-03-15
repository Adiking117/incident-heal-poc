# alert_webhook_async.py
from fastapi import FastAPI, Request
import aio_pika
import json

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Create a robust connection at startup
    app.state.connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")

@app.on_event("shutdown")
async def shutdown_event():
    # Close connection cleanly
    await app.state.connection.close()

@app.post("/alert")
async def receive_alert(request: Request):
    data = await request.json()
    print("🚨 Alert received:", data)

    try:
        # Open channel from the shared connection
        async with app.state.connection.channel() as channel:
            # Ensure queue exists
            await channel.declare_queue("incidents", durable=True)

            # Publish message
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(data).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key="incidents"
            )

        return {"status": "sent to rabbitmq"}

    except Exception as e:
        print("❌ Error publishing to RabbitMQ:", e)
        return {"status": "error", "detail": str(e)}