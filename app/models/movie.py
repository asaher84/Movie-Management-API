
import uuid
from sqlalchemy import Column, String, Integer, Float
from app.dao.db import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False, index=True)
    director = Column(String, nullable=True)
    releaseYear = Column(Integer, nullable=True)
    genre = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
