from typing import Optional, Dict
from pydantic import BaseModel, Field


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
    idol_details: Dict[str, IdolDetailsBase] = Field(example="""
        {
            "image_1": {
            "name": "string",
            "age": 0,
            "dob": "string",
            "group": "string",
            "summary": "string"
            },
            "image_2": {
            "name": "string",
            "age": 0,
            "dob": "string",
            "group": "string",
            "summary": "string"
            },
            "image_3": {
            "name": "string",
            "age": 0,
            "dob": "string",
            "group": "string",
            "summary": "string"
            }
        }
    """)
