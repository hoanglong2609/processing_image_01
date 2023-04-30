from fastapi import APIRouter
from model.result import Result as ResultModel
from model.image import Image
from schemas import result as result_schemas
from typing import List
from base64 import b64decode
from utils.db import transaction
from playhouse.shortcuts import model_to_dict


router = APIRouter()


@router.get('/')
def get_result():
    return ResultModel.get_list()


@router.post('/')
@transaction
def create_result(result: result_schemas.ResultCreate):
    data = {
        'code': result.code,
        'subject': result.subject,
        'result': result.result,
    }
    result_exists = ResultModel.get_or_none(code=result.code, subject=result.subject)
    if result_exists:
        return ResultModel.update_one(result_exists.id, None, data)
    return ResultModel.create(None, **data)
