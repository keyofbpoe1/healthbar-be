# http://docs.peewee-orm.com/en/latest/peewee/quickstart.html#quickstart
# import * means import everything from peewee

from peewee import *
import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import urllib3
from playhouse.postgres_ext import *

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# postgres admin password
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

# to connect to sqllite:
# DATABASE = SqliteDatabase('dogs.sqlite')
# to connect to postgres, use below and set up postgres db in pgadmin
DATABASE = PostgresqlDatabase('healthbar_db', user='postgres', password=DATABASE_PASSWORD)

class User(Model):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(index=True)
    bio = TextField()
    pic = TextField()
    role = CharField()
    class Meta:
        database = DATABASE
        table_name = 'users_tbl'

class Tag(Model):
    label = CharField()
    # article = ForeignKeyField(Article, backref='tags')
    class Meta:
        database = DATABASE
        table_name = 'tags_tbl'

class Article(Model):
    author = ForeignKeyField(User, backref='articles')
    category = CharField()
    title = CharField()
    body = TextField()
    pics = ArrayField(TextField, null=True)
    tags = ArrayField(ForeignKeyField, {'model': Tag, 'field_type': 'id'}, null=True)
    endorsements = ArrayField(CharField, null=True)
    discussion = ArrayField(CharField, null=True)
    class Meta:
        database = DATABASE
        table_name = 'articles_tbl'

class Discussion(Model):
    author = ForeignKeyField(User)
    body = TextField()
    article = ForeignKeyField(Article, backref='discussion')
    class Meta:
        database = DATABASE
        table_name = 'discussion_tbl'

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Tag, User, Article, Discussion], safe=True)
    print("TABLES Created")
    DATABASE.close()

# one to many
###################################
# user to article
# user to discussion
# article to discussion

# many to many
#################################
# articled to tags
# users to pinned articles 
