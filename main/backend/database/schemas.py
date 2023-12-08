from typing import Optional, Dict
from pydantic import BaseModel

class UploadStatusBase(BaseModel):
    result: str

class UploadStatus(UploadStatusBase):
    path: list[Optional[str]] = None
    failure_reason: Optional[str] = None

# class ImageRetrivalBase(BaseModel):
#     blobstr: str


class IdolDetailsBase(BaseModel):
    name: str
    age: int
    dob: str
    group: str
    summary: str

class IdolDetails(BaseModel):
    idol_details: Dict[str, IdolDetailsBase]




