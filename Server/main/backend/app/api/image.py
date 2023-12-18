import os

from typing import Annotated
import uuid

from fastapi import APIRouter, Depends
from fastapi import File, UploadFile
from sqlalchemy.orm import Session
import requests

from database import schemas, crud
from database.database import get_db

from dotenv import load_dotenv

import json

load_dotenv()

AI_IP = os.getenv("AI_IP")

IMAGE_FOLDER_PATH = "./images"

router = APIRouter()


# TODO: To replace all 'breaks' with raise response
@router.post("/uploadfiles/", response_model=schemas.UploadStatus, response_model_exclude_none=True)
async def create_upload_files(
    files: Annotated[list[UploadFile], File(description="Multiple files as UploadFile")], db: Session = Depends(get_db),
):

    path = []
    status = False

    for file in files:
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
                        break

                if res.status_code == 422:
                    print("something went wrong..")
        else:
            break

    return {"result": "successfully uploaded", "path": path} if status else {"result": "failed to upload", "failure_reason": "..?"}


@router.get("/getidoldetails/{image_path}", response_model=schemas.IdolDetails)
async def test(image_path: str, db: Session = Depends(get_db)):
    res = await crud.retrieve_idol_details(db, image_path)
    data = {}
    for i in res:
        data = i[0].data

    formatted_data = {"idol_details":
                      json.loads(data)
                      }

    print(formatted_data)
    return formatted_data
