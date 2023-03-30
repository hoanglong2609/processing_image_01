from schemas.base import BaseSchemas


class Subject(BaseSchemas):
    id: int
    name: str


class SubjectCreate(BaseSchemas):
    name: str
