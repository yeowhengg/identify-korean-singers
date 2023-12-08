from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi import File, UploadFile
from sqlalchemy.orm import Session
import uuid

from database import models, schemas, crud
from database.database import get_db

router = APIRouter()

IMAGE_FOLDER_PATH = "./images"

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
        
        try:
            status = await crud.insert_image_data(db, full_image_path)
            if status:
                with open(full_image_path, "wb") as f:
                    f.write(content)
                path.append(full_image_path)
        except Exception as e:
            break
    
    return {"result": "successfully uploaded", "path":path} if status else {"result": "failed to upload"}


