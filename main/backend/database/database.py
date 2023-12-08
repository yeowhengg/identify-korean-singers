from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} #only needed for SQLite. If we're using other database, this is not needed
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # creates an instance of a database session

Base = declarative_base() # for ORM models creation

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()