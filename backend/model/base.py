from peewee import Model
from config.database import db
from operator import attrgetter


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def get_list(cls, **kwargs):
        query = cls.handle_select(**kwargs)

        for key, value in kwargs.items():
            if key in cls._meta.fields:
                if value is not None:
                    query = query.where(attrgetter(key)(cls) == value)
            if key == 'search_info' and value:
                if value != '':
                    query = query.where(cls.name.contains(value.lower()))
        query = query.dicts()

        return list(query)

    @classmethod
    def handle_select(cls, **kwargs):
        return cls.select()
