from mongoengine import Document, StringField, BooleanField, connect

connect(
    "contacts_db",
    host="mongodb+srv://xofoc41187:FL2FPv52lX2LZgfJ@cluster0.8o92hua.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)
    phone_number = StringField()
    preferred_method = StringField(choices=["email", "sms"], default="email")
