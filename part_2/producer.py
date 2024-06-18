import pika
import json
from faker import Faker
from models import Contact
from typing import Any, Dict

fake = Faker()


def create_contact() -> Contact:
    contact: Contact = Contact(
        fullname=fake.name(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        preferred_method=fake.random_element(elements=("email", "sms")),
    )
    contact.save()
    return contact


def send_to_queue(contact_id: str, method: str) -> None:
    connection: pika.BlockingConnection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost")
    )
    channel: pika.adapters.blocking_connection.BlockingChannel = connection.channel()
    queue_name: str = "email_queue" if method == "email" else "sms_queue"
    channel.queue_declare(queue=queue_name)

    message: Dict[str, Any] = {"contact_id": str(contact_id)}
    channel.basic_publish(exchange="", routing_key=queue_name, body=json.dumps(message))
    connection.close()


if __name__ == "__main__":
    num_contacts: int = 10  # Number of contacts to generate
    for _ in range(num_contacts):
        contact: Contact = create_contact()
        send_to_queue(contact.id, contact.preferred_method)
