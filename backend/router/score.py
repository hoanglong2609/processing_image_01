from typing import List
from fastapi import APIRouter
from model.score import Score as ScoreModel
from schemas import score as score_schemas


router = APIRouter()


@router.get('/', response_model=List[score_schemas.Score])
def get_scores():
    return ScoreModel.get_list()
