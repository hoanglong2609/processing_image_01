from model.base import BaseModel
from peewee import CharField, IntegerField, AnyField, fn, SQL
from model.subject import Subject
from operator import attrgetter


class User(BaseModel):
    code = CharField()
    password = CharField()
    name = CharField()
    subject_ids = AnyField()
    role = IntegerField()

    class Meta:
        db_table = 'user'

    @classmethod
    def handle_select(cls, **kwargs):
        query = (
            cls.select(
                cls.id,
                cls.code,
                cls.name,
                cls.role,
                fn.array_agg(
                    fn.json_build_object(
                        'id', Subject.id,
                        'name', Subject.name
                    )
                ).alias('subjects')
            ).join(
                Subject, on=Subject.id == fn.any(cls.subject_ids)
            ).group_by(
                cls.id
            )
        )

        if 'subject' in kwargs and kwargs['subject']:
            query = query.where(SQL(f"{kwargs['subject']} = any(subject_ids)"))

        return query

