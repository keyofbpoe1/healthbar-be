# http://docs.peewee-orm.com/en/latest/peewee/quickstart.html#quickstart
# import * means import everything from peewee

from peewee import *
import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv
# import json
# import urllib3
from playhouse.postgres_ext import *
from playhouse.db_url import connect
from flask_login import UserMixin

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# postgres admin password
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

# to connect to sqllite:
# DATABASE = SqliteDatabase('healthbar.sqlite')
# to connect to postgres, use below and set up postgres db in pgadmin
# DATABASE = PostgresqlDatabase('healthbar_db', user='postgres', password=DATABASE_PASSWORD)
DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///healthbar.sqlite')
# DATABASE = connect('sqlite:///healthbar.sqlite')


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(index=True)
    bio = TextField(null=True)
    user_avatar = CharField()
    role = CharField()
    class Meta:
        database = DATABASE
        table_name = 'users_tbl'


class Article(Model):
    author = ForeignKeyField(User, backref='articles')
    category = CharField()
    title = CharField()
    body = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    # pics = ArrayField(TextField, null=True)
    class Meta:
        database = DATABASE
        table_name = 'articles_tbl'

class Tag(Model):
    tag = CharField()
    class Meta:
        database = DATABASE
        table_name = 'tags_tbl'

class Tagjunction(Model):
    tag = ForeignKeyField(User, backref='tags')
    article = ForeignKeyField(Article, backref='tags')
    class Meta:
        database = DATABASE
        table_name = 'tagjunction_tbl'

class Discussion(Model):
    author = ForeignKeyField(User, backref='discussions')
    article = ForeignKeyField(Article, backref='discussions')
    comment = CharField()
    class Meta:
        database = DATABASE
        table_name = 'discussion_tbl'

class Endorsement(Model):
    endorser = ForeignKeyField(User, backref= 'endorsements')
    article = ForeignKeyField(Article, backref='endorsements')
    class Meta:
        database = DATABASE
        table_name = 'endorsements_tbl'

class Pin(Model):
    pinner = ForeignKeyField(User, backref= 'pins')
    article = ForeignKeyField(Article, backref='pins')
    pingroup = CharField()
    class Meta:
        database = DATABASE
        table_name = 'pins_tbl'

class Image(Model):
    user = ForeignKeyField(User, backref= 'avatar', null=True)
    imgtype = CharField()
    article = ForeignKeyField(Article, backref='images', null=True)
    class Meta:
        database = DATABASE
        table_name = 'images_tbl'

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Article, Discussion], safe=True)
    print("TABLES Created")
    DATABASE.close()

# one to many
###################################
# user to article
# user to discussion
# article to discussion
# user to image
# article to images

# many to many
#################################
# articled to tags
# users to pinned articles
