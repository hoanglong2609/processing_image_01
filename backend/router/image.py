from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter()


@router.get('/')
def get_image(path):
    return FileResponse(path)
