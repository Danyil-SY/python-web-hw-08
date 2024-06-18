import pika
import json
from models import Contact
from typing import Any, Dict


def send_email(contact: Contact) -> None:
    print(f"Sending email to {contact.fullname} at {contact.email}")
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
        send_email(contact)


connection: pika.BlockingConnection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)
channel: pika.adapters.blocking_connection.BlockingChannel = connection.channel()
channel.queue_declare(queue="email_queue")
channel.basic_consume(queue="email_queue", on_message_callback=callback, auto_ack=True)

print("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
