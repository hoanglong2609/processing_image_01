from model.base import BaseModel
from peewee import FloatField, ForeignKeyField, IntegerField, fn
from playhouse.postgres_ext import ArrayField
from playhouse.shortcuts import model_to_dict
from model.image import Image
from model.user import User
from model.subject import Subject
from model.result import Result
from base64 import b64decode
from fastapi import HTTPException
from utils.my_csv import write_csv
from fastapi.responses import FileResponse
from operator import attrgetter


class Score(BaseModel):
    student = ForeignKeyField(User)
    image = ForeignKeyField(Image)
    score = FloatField()
    filled_cell = ArrayField()
    subject = ForeignKeyField(Subject)
    code = IntegerField()

    @classmethod
    def create(cls, image, code, subject, student, filled_cell):
        image = Image.create(b64decode(image)).id
        student = User.get_or_none(code=student)
        if not student:
            raise HTTPException(400, 'student not exists')

        # get result
        result = Result.get_or_none(code=code, subject=subject)
        if not student:
            raise HTTPException(400, 'student not exists')
        if not result:
            raise HTTPException(400, 'result not exists')
        result = model_to_dict(result)

        score = 0
        for index, cell in enumerate(result['result']):
            if index < len(filled_cell):
                score += (1 if cell == filled_cell[index] else 0)

        score = score / len(result['result']) * 10

        data = {
            'student': student.id,
            'code': code,
            'subject': subject,
            'filled_cell': filled_cell,
            'score': score,
            'image': image
        }
        return super().create(**data)

    @classmethod
    def update_one(cls, id, image, code, subject, student, filled_cell):
        result = Result.get_or_none(subject=subject, code=code)
        image = Image.create(b64decode(image)).id
        if not student:
            raise HTTPException(400, 'result not exists')
        result = model_to_dict(result)

        score = 0

        for index, cell in enumerate(result['result']):
            if index < len(filled_cell):
                score += (1 if cell == filled_cell[index] else 0) / len(result['result']) * 10

        data = {
            'student': student,
            'code': code,
            'subject': subject,
            'filled_cell': filled_cell,
            'score': score,
            'image': image
        }

        return cls.update(**data).where(cls.id == id).execute()

    @classmethod
    def update_by_subject_and_code(cls, subject, code):
        scores = cls.get_list(subject=subject, code=code)
        result = Result.get_or_none(subject=subject, code=code)

        if not result:
            raise HTTPException(400, 'no result')

        for score_data in scores:
            # print(score_data)
            score = 0
            for index, cell in enumerate(score_data['filled_cell']):
                if index < len(result.result):
                    score += (1 if cell == result.result[index] else 0)
            cls.update(**{'score': score}).where(cls.id == score_data['id']).execute()

    @classmethod
    def get_list(cls, **kwargs):
        query = cls.handle_select(**kwargs)

        for key, value in kwargs.items():
            if key in cls._meta.fields:
                if value is not None:
                    query = query.where(attrgetter(key)(cls) == value)

        query = query.dicts()
        scores = list(query)

        for score in scores:
            result_id = Result.get_or_none(code=score['code'], subject=score['subject']['id'])
            if result_id:
                score['result'] = result_id.result

        return scores

    @classmethod
    def handle_select(cls, **kwargs):
        return (
            cls.select(
                cls.id,
                fn.json_build_object(
                    'id', User.id, 'name', User.name, 'code', User.code, 'mail', User.mail
                ).alias('student'),
                cls.code,
                cls.score,
                fn.json_build_object(
                    'id', Subject.id, 'name', Subject.name
                ).alias('subject'),
                cls.filled_cell,
                fn.json_build_object(
                    'id', Image.id, 'url', Image.url
                ).alias('image')
            ).left_outer_join(
                User, on=User.id == cls.student
            ).left_outer_join(
                Subject, on=Subject.id == cls.subject
            ).left_outer_join(
                Image, on=Image.id == cls.image
            )
        )

    @classmethod
    def to_csv(cls, subject):
        scores = cls.get_list(subject=subject)

        fields = ['id', 'subject', 'code', 'name', 'mail', 'score']
        header = fields
        rows = [header]
        print(scores)
        if not scores:
            raise HTTPException(400, 'Khong co diem')

        # items of csv
        for score in scores:
            rows.append([
                score['id'],
                score['subject']['name'],
                score['student']['code'],
                score['student']['name'],
                score['student']['mail'],
                score['score'],
            ])
        # render csv
        path = 'tmp/example.csv'
        write_csv('tmp/example.csv', rows)
        return FileResponse(path, media_type='application/octet-stream')
