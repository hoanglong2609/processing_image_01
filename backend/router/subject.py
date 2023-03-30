from fastapi import APIRouter
from model.subject import Subject
from schemas import subject as subject_schemas
from typing import List
from playhouse.shortcuts import model_to_dict

router = APIRouter()


@router.get('/', response_model=List[subject_schemas.Subject])
def get_subject():
    return Subject.get_list()


@router.post('/create')
def create_subject(subject: subject_schemas.SubjectCreate):
    return model_to_dict(Subject.create(**subject.dict()))

