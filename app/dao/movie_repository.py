
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.movie import Movie

class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, movie: Movie) -> Movie:
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def get(self, movie_id: str) -> Optional[Movie]:
        return self.db.get(Movie, movie_id)

    def list(self, limit: int, offset: int) -> Tuple[List[Movie], int]:
        total = self.db.scalar(select(func.count()).select_from(Movie)) or 0
        items = self.db.execute(select(Movie).limit(limit).offset(offset)).scalars().all()
        return items, total

    def update(self, movie: Movie) -> Movie:
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def delete(self, movie: Movie) -> None:
        self.db.delete(movie)
        self.db.commit()
