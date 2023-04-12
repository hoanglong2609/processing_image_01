from model.base import BaseModel
from peewee import IntegerField, CharField, ForeignKeyField, fn
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

    @classmethod
    def handle_select(cls, **kwargs):
        query = (
            cls.select(
                cls.id,
                cls.code,
                fn.json_build_object(
                    'id', Subject.id,
                    'name', Subject.name
                ).alias('subject'),
                cls.result,
                fn.json_build_object(
                    'id', Image.id,
                    'url', Image.url
                ).alias('image')
            ).join(
                Subject, on=Subject.id == cls.subject
            ).join(
                Image, on=Image.id == cls.image
            )
        )

        return query
