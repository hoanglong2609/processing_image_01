from fastapi import APIRouter
from router import user, processing_image, subject, result, image, score

router = APIRouter()

router.include_router(
    user.router,
    prefix='/user',
    tags=['User']
)

router.include_router(
    subject.router,
    prefix='/subject',
    tags=['subject']
)

router.include_router(
    image.router,
    prefix='/image',
    tags=['image']
)

router.include_router(
    result.router,
    prefix='/result',
    tags=['result']
)

router.include_router(
    score.router,
    prefix='/score',
    tags=['score']
)

router.include_router(
    processing_image.router,
    prefix='/processing_image',
    tags=['processing_image']
)

# router.include_router(
#     student.router,
#     prefix= '/student',
#     tags=['Student']
# )

