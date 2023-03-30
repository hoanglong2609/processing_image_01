from model.base import BaseModel
from peewee import IntegerField, CharField, ForeignKeyField
from playhouse.postgres_ext import ArrayField
from model.image import Image
from model.subject import Subject
from playhouse.shortcuts import model_to_dict
from base64 import b64decode


class Result(BaseModel):
    code = IntegerField()
    image = ForeignKeyField(Image)
    subject = ForeignKeyField(Subject)
    result = ArrayField()

    @classmethod
    def create(cls, image, **kwargs):
        image = Image.create(b64decode(image))

        kwargs['image'] = image.id
        return model_to_dict(super().create(**kwargs))
