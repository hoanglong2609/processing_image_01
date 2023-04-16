from model.base import BaseModel
from peewee import CharField, IntegerField, AnyField


class Subject(BaseModel):
    name = CharField()
    password = CharField()

