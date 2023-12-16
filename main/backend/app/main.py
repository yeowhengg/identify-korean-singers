from fastapi import FastAPI

from .api import image

from database import models
from database.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
def start_up():
    get_db()


app.include_router(image.router)


@app.get("/")
async def main():
    return "HELLO WORLD"
