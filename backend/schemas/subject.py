from schemas.base import BaseSchemas


class Subject(BaseSchemas):
    id: int
    name: str
    password: str


class SubjectCreate(BaseSchemas):
    name: str
    password: str


class Login(BaseSchemas):
    id: str
    password: str
