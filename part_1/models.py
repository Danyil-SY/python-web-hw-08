from mongoengine import Document, StringField, ReferenceField, ListField, connect

connect(
    "authors_db",
    host="mongodb+srv://xofoc41187:esbXDApf7ibao2bF@cluster0.ihsopqr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)
