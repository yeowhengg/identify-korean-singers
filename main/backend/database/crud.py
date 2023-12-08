from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas


async def insert_image_data(db: Session, image_data: schemas.UploadStatus):
    data_to_insert = models.ImagePath(path = image_data)

    try:
        db.add(data_to_insert)
        db.commit()
        db.refresh(data_to_insert)
        return True
    
    except Exception as e:
        return False
    
async def processed_idols(db: Session, image_to_update):
    upd = update(models.ImagePath)
    cond = upd.where(models.ImagePath.path == image_to_update)
    val = cond.values(is_processed=True)
    db.execute(val)
    db.commit()
    return False