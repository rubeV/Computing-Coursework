import datetime
from playhouse.migrate import *

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *
import os.path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "user.db")
DATABASE = SqliteDatabase(db_path)


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    fplID = IntegerField(default=000000)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    @classmethod
    def create_user(cls, username, email, fplID, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    fplID=fplID,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")


def initialize():
    DATABASE.connect()
    print("connected")
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()
