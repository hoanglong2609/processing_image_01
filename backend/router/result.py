from fastapi import APIRouter
from model.result import Result as ResultModel
from model.image import Image
from schemas import result as result_schemas
from typing import List
from base64 import b64decode
from utils.db import transaction
from playhouse.shortcuts import model_to_dict


router = APIRouter()


@router.get('/', response_model=List[result_schemas.Result])
def get_result():
    return ResultModel.get_list()


@router.post('/')
@transaction
def create_result(result: result_schemas.ResultCreate):
    image = Image.create(b64decode(result.image))

    result.image = image.id
    result = result.dict()
    return model_to_dict(ResultModel.create(**result))
