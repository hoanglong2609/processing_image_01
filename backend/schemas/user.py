from schemas.base import BaseSchemas
from typing import List


class User(BaseSchemas):
    id: int
    code: str
    name: str
    password: str
    subject_ids: List[int]
    role: int


class UserCreate(BaseSchemas):
    code: str
    name: str
    password: str
    subject_ids: List[int]
    role: int
    mail: str


class UserUpdate(BaseSchemas):
    code: str
    name: str
    subject_ids: List[int]
    role: int
    mail: str

