import peewee
from datetime import datetime

db = peewee.SqliteDatabase('db.sqlite3')

class BaseModel(peewee.Model):
    class Meta:
        database = db


class ShortenLink(BaseModel):
    u_id: str = peewee.TextField(null = True)
    link: str = peewee.TextField(null = True)

class RequestedLink(BaseModel):
    message_id: str = peewee.TextField(null = True)
    chat_id: str = peewee.TextField(null = True)
    link: str = peewee.TextField(null = True)
    send_time: datetime = peewee.DateTimeField(null = True)

db.connect()
db.create_tables([
    ShortenLink, RequestedLink
])
