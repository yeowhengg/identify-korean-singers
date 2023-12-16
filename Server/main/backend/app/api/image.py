from typing import Annotated
import uuid

from fastapi import APIRouter, Depends
from fastapi import File, UploadFile
from sqlalchemy.orm import Session
import requests

from database import schemas, crud
from database.database import get_db

router = APIRouter()

IMAGE_FOLDER_PATH = "./images"


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
                print(full_image_path)
                read_files = {"file": (full_image_path, f.read())}
                res = requests.post("http://127.0.0.1:8001", files=read_files)
                if res.status_code == 200:
                    update_status = await crud.processed_idols(db, full_image_path)
                    if update_status is False:
                        break

                if res.status_code == 422:
                    print("something went wrong..")
        else:
            break

    return {"result": "successfully uploaded", "path": path} if status else {"result": "failed to upload", "failure_reason": "..?"}


@router.post("/sendidoldetails/", response_model=schemas.IdolDetails)
def test(data: schemas.IdolDetails):
    return data
