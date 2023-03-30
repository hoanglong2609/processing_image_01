from fastapi import APIRouter
from model.user import User
from schemas import user as users_chemas
from playhouse.shortcuts import model_to_dict
from schemas.login import Login

router = APIRouter()


@router.get('/')
def get_account(subject: int = None):
    return User.get_list(subject=subject)


@router.post('/create')
def create_account(user: users_chemas.UserCreate):
    return model_to_dict(User.create(**user.dict()))


@router.post('/login')
def sign_in(user: Login):
    """User login"""
    query = User.get_list(**user.dict())
    if len(query):
        return {"code": 200, "data": query}
    else:
        return {"code": 400, "data": query}
