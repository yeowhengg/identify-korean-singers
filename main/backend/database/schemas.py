from typing import Optional

from pydantic import BaseModel

class UploadStatusBase(BaseModel):
    result: str

class UploadStatus(UploadStatusBase):
    path: list[Optional[str]] = None


