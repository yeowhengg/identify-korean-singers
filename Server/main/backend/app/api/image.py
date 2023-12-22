import os

from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, Request
from fastapi import File, UploadFile
from sqlalchemy.orm import Session
import requests

from utils.exceptions import ExceptionHandling as ExceptionHandling

from database import schemas, crud
from database.database import get_db

from dotenv import load_dotenv

import json


load_dotenv()

AI_IP = os.getenv("AI_IP")

IMAGE_FOLDER_PATH = "./images"

router = APIRouter()


# TODO: To replace all 'breaks' with raise response


@router.post("/uploadfiles/",  response_model=schemas.UploadStatusBase | schemas.EmptyFileUploaded)
async def create_upload_files(
    files: Annotated[list[UploadFile], File(description="Multiple files as UploadFile")], db: Session = Depends(get_db),
):

    path = []
    check_file = [file for file in files if file.headers.get(
        "content-type") == "image/jpeg"]

    if len(check_file) != len(files):
        raise ExceptionHandling.NOT_IMAGE_EXCEPTION

    for file in check_file:
        filename = f"{uuid.uuid4()}.jpg"
        content = await file.read()
        full_image_path = f"{IMAGE_FOLDER_PATH}/{filename}"
        status = await crud.insert_image_data(db, full_image_path)

        if status:
            with open(full_image_path, "wb") as f:
                f.write(content)
            path.append(full_image_path)

            with open(full_image_path, 'rb') as f:
                read_files = {"file": (full_image_path, f.read())}
                res = requests.post(AI_IP, files=read_files)

                if res.status_code == 200:
                    update_status = await crud.processed_idols(db, full_image_path)
                    if update_status is False:
                        raise ExceptionHandling.INTERNAL_EXCEPTION

                if res.status_code == 422:
                    raise ExceptionHandling.INTERNAL_EXCEPTION

        else:
            raise ExceptionHandling.INTERNAL_EXCEPTION

    return {"path": path}


@router.get("/getidoldetails/{image_path}", response_model=schemas.IdolDetails)
async def test(image_path: str, db: Session = Depends(get_db)):
    res = await crud.retrieve_idol_details(db, image_path)

    if res is False:
        raise ExceptionHandling.IMAGE_NOT_FOUND_EXCEPTION

    data = {}

    for i in res:
        data = i.data

    formatted_data = {"idol_details":
                      json.loads(data)
                      }

    return formatted_data
