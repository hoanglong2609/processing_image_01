from fastapi import APIRouter
from model.subject import Subject
from schemas import subject as subject_schemas
from typing import List
from playhouse.shortcuts import model_to_dict

router = APIRouter()


@router.get('/', response_model=List[subject_schemas.Subject])
def get_subject(id=None):
    return Subject.get_list(id=id)


@router.post('/create')
def create_subject(subject: subject_schemas.SubjectCreate):
    return model_to_dict(Subject.create(**subject.dict()))


@router.put('/{id}')
def update_subject(id: int, subject: subject_schemas.SubjectCreate):
    return Subject.update(**subject.dict()).where(Subject.id == id).execute()


@router.post('/login')
def sign_in(subject: subject_schemas.Login):
    """User login"""
    query = Subject.get_list(**subject.dict())
    if query:
        return {"code": 200, "data": query[0]}
    else:
        return {"code": 400, "data": query}
