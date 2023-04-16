from datetime import datetime

from mongoengine import *
from mongoengine import EmbeddedDocument, Document
from mongoengine import connect
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'USER')
mongodb_pass = config.get('DB', 'PASSWORD')
db_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')


connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)


class Author(Document):
    fullname = StringField(required=True)
    born_date = DateTimeField()
    born_location = StringField(max_length=500)
    description = StringField()


class Quote(Document):
    tags = ListField(StringField(max_length=200))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {'allow_inheritance': True}
