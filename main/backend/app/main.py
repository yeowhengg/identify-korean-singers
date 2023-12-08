from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .api import image

from database import models, schemas, crud
from database.database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
def start_up():
    get_db()

app.include_router(image.router)


@app.get("/")
async def main():
    return "HELLO WORLD"

