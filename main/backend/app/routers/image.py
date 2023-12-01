from typing import Annotated
from fastapi import APIRouter
from fastapi import File, UploadFile
import uuid

router = APIRouter()

test_db = {"image_path": [], "image_byte": []}

IMAGE_FOLDER_PATH = "./images"

@router.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):

    for file in files:
        filename = f"{uuid.uuid4()}.jpg"
        content = await file.read()
        full_image_path = f"{IMAGE_FOLDER_PATH}/{filename}"

        with open(full_image_path, "wb") as f:
            f.write(content)

        test_db["image_path"].append(full_image_path)
        test_db["image_byte"].append(content)

    print(test_db)
    return {"Images uploaded!"}


