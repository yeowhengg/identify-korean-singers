from sqlalchemy import update, select
from sqlalchemy.orm import Session
from . import models, schemas
import json

# when AI server is done and set up, this function will be called after it sends back the details


async def insert_image_data(db: Session, upload_status: schemas.UploadStatus):
    data_to_insert = models.ImagePath(path=upload_status)

    try:
        db.add(data_to_insert)
        db.commit()
        db.refresh(data_to_insert)
        return True

    except Exception as e:
        return False


async def processed_idols(db: Session, image_to_update):
    import random as ran
    ran_num = ran.randint(1, 99999999)
    upd = update(models.ImagePath)
    cond = upd.where(models.ImagePath.path == image_to_update)
    val = cond.values(is_processed=True, data=json.dumps({
        "idol_1": {
            "name": "string " + str(ran_num),
            "age": 0,
            "dob": "27-11-1999",
            "group": "random...",
            "summary": "soemthing here..."
        }
    })

    )
    db.execute(val)
    db.commit()
    return True


async def retrieve_idol_details(db: Session, path):
    updated_path = "./images/"+path

    stmt = select(models.ImagePath).where(
        models.ImagePath.path == updated_path)
    result = db.execute(stmt)

    return result
