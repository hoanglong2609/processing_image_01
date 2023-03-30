from fastapi import FastAPI
from router import api
from config.database import db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
def startup():
    if db.is_closed():
        db.connect()


@app.on_event('shutdown')
def shutdown():
    if not db.is_closed():
        db.close()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


app.include_router(api.router)
