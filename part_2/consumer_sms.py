import pika
import json
from models import Contact
from typing import Any, Dict


def send_sms(contact: Contact) -> None:
    print(f"Sending SMS to {contact.fullname} at {contact.phone_number}")
    contact.sent = True
    contact.save()


def callback(
    ch: pika.adapters.blocking_connection.BlockingChannel,
    method: pika.spec.Basic.Deliver,
    properties: pika.spec.BasicProperties,
    body: bytes,
) -> None:
    message: Dict[str, Any] = json.loads(body)
    contact: Contact = Contact.objects(id=message["contact_id"]).first()
    if contact:
        send_sms(contact)


connection: pika.BlockingConnection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)
channel: pika.adapters.blocking_connection.BlockingChannel = connection.channel()
channel.queue_declare(queue="sms_queue")
channel.basic_consume(queue="sms_queue", on_message_callback=callback, auto_ack=True)

print("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
