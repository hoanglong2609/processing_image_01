from schemas.base import BaseSchemas
from typing import List


class Score(BaseSchemas):
    student: int
    image: str
    score: float
    filled_cell: List[int]
