from fastapi import FastAPI
import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{request}: {exc_str}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
