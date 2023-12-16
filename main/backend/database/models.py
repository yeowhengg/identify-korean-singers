from sqlalchemy import Boolean, Column, Integer, String
from .database import Base


class ImagePath(Base):
    __tablename__ = "Image"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, index=True)
    is_processed = Column(Boolean, default=False)
