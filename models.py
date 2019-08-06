from datetime import datetime
from mongoengine import (
    connection,
    Document,
    DynamicDocument,
    StringField,
    DateTimeField,
    ImageField,
    URLField
)


connection('test_db_mongo')


class Post(Document):
    title = StringField(max_length=200, required=True)
    post = StringField(max_length=5000)
    image = ImageField()
    url = URLField()

    date_created = DateTimeField(defaut=datetime.utchow)
