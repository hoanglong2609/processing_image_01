from typing import List
from fastapi import APIRouter
from model.score import Score as ScoreModel
from schemas import score as score_schemas

router = APIRouter()


@router.get('/')
def get_scores(student: int = None, subject: int = None):
    return ScoreModel.get_list(student=student, subject=subject)


@router.get('/csv')
def down_load_csv(subject: int):
    return ScoreModel.to_csv(subject=subject)
