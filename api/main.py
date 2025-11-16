from fastapi import FastAPI
from pydantic import BaseModel
import json
import pika

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "notifications"

app = FastAPI(title="Event-Driven Notification API")

class Notification(BaseModel):
    user_id: str
    channel: str
    message: str
    force_fail: bool | None = False

def publish_notification(notification: Notification):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    body = json.dumps(notification.dict())
    channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=body)
    connection.close()

@app.post("/notifications")
def create_notification(notification: Notification):
    publish_notification(notification)
    return {"status": "queued", "notification": notification}
