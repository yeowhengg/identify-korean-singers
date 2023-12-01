from fastapi import Depends, FastAPI

from .routers import image

app = FastAPI()


app.include_router(image.router)


@app.get("/")
async def main():
    return "HELLO WORLD"

