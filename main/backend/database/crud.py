from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas


def get_image_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ImagePath).offset(skip).limit(limit).all()

async def insert_image_data(db: Session, image_data: schemas.UploadStatus):
    data_to_insert = models.ImagePath(path = image_data)

    try:
        db.add(data_to_insert)
        db.commit()
        db.refresh(data_to_insert)
        return True
    
    except Exception as e:
        return False