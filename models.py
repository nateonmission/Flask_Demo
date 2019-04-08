import datetime
from peewee import *
from flask_login import UserMixin
from passlib.hash import sha256_crypt
# from bcrypt import hashpw, gensalt


DATABASE = SqliteDatabase('aq.db')


class User(UserMixin, Model):
    id = AutoField(unique=True)
    first_name = CharField(unique=True)
    last_name = CharField(unique=True)
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    @classmethod
    def create_user(cls, first_name, last_name, username, email, password, admin=False):
        try:
            cls.create(
                # id=id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=sha256_crypt.encrypt(password.encode('utf-8')),
                joined_at=datetime.datetime.now(),
                is_admin=admin
            )
        except IntegrityError:
            raise ValueError("User Exists")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables(['user'], safe=True)
    DATABASE.close()
