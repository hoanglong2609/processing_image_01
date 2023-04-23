from fastapi import APIRouter, HTTPException
from model.user import User
from schemas import user as users_chemas
from playhouse.shortcuts import model_to_dict
from schemas.login import Login
from utils.mail import send_mail

router = APIRouter()


@router.get('/')
def get_account(id: int = None, subject: int = None, role: int = None, search_info: str = None):
    return User.get_list(id=id, subject=subject, role=role, search_info=search_info)


@router.get('/forgot')
def forgot_password(code, gmail: str):
    # get pass
    user = User.get_or_none(code=code, mail=gmail)
    if not user:
        raise HTTPException(400, 'no user')

    password = user.password
    send_mail(password, gmail)


@router.post('/')
def create_account(user: users_chemas.UserCreate):
    # check duplicate
    if list(User.select().where(User.code == user.code)):
        raise HTTPException(400, 'duplicate code')
    return model_to_dict(User.create(**user.dict()))


@router.post('/change_password')
def change_password(payload: users_chemas.ChangePassword):
    user = User.get_or_none(id=payload.id, password=payload.old_password)
    if not user:
        raise HTTPException(400, 'wrong password')
    User.update(password=payload.new_password).where(User.id == payload.id).execute()


@router.post('/login')
def sign_in(user: Login):
    """User login"""
    query = User.get_list(**user.dict())
    if query:
        return {"code": 200, "data": query[0]}
    else:
        return {"code": 400, "data": query}


@router.put('/{id}')
def update_user(id: int, user: users_chemas.UserUpdate):
    return User.update(**user.dict()).where(User.id == id).execute()


@router.delete('/{id}')
def delete_user(id: int):
    return User.delete_by_id(id)
