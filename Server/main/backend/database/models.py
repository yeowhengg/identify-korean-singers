from sqlalchemy import Boolean, Column, Integer, String, JSON
from .database import Base


class ImagePath(Base):
    __tablename__ = "Image"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, index=True)
    is_processed = Column(Boolean, default=False)
    data = Column(String, index=True)
