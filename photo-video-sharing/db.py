from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# postgress connection
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/photo_video"

#create engine 
engine = create_engine(DATABASE_URL)

#SesionLocal class
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

#Base class for models
Base = declarative_base()

#Dependency for fast api routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()