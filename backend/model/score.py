from model.base import BaseModel
from peewee import FloatField, ForeignKeyField, IntegerField
from playhouse.postgres_ext import ArrayField
from playhouse.shortcuts import model_to_dict
from model.image import Image
from model.user import User
from model.subject import Subject
from model.result import Result
from base64 import b64decode
from fastapi import HTTPException


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
