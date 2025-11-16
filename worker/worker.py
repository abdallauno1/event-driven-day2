
import json
import time
import pika
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}',
    stream=sys.stdout
)

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "notifications"

def process_notification(data):
    if data.get("force_fail") is True:
        raise ValueError("Simulated processing error")
    logging.info(f"Processing notification for user={data['user_id']}, channel={data['channel']}")
    time.sleep(1)

def callback(ch, method, properties, body):
    data = json.loads(body)
    try:
        process_notification(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Error processing message: {str(e)} — retrying later")
        time.sleep(1)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    logging.info("Worker starting — waiting for messages...")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    channel.start_consuming()

if __name__ == "__main__":
    main()
