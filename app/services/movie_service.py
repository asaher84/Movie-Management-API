
from typing import List, Tuple
from app.dao.movie_repository import MovieRepository
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieUpdate
from fastapi import HTTPException, status

class MovieService:
    def __init__(self, repo: MovieRepository):
        self.repo = repo

    def create_movie(self, payload: MovieCreate) -> Movie:
        movie = Movie(
            title=payload.title,
            director=payload.director,
            releaseYear=payload.releaseYear,
            genre=payload.genre,
            rating=payload.rating,
        )
        return self.repo.create(movie)

    def get_movie(self, movie_id: str) -> Movie:
        movie = self.repo.get(movie_id)
        if not movie:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
        return movie

    def list_movies(self, limit: int, offset: int) -> Tuple[List[Movie], int]:
        return self.repo.list(limit=limit, offset=offset)

    def update_movie(self, movie_id: str, payload: MovieUpdate) -> Movie:
        movie = self.repo.get(movie_id)
        if not movie:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
        data = payload.model_dump(exclude_unset=True)
        for k, v in data.items():
            setattr(movie, k, v)
        return self.repo.update(movie)

    def delete_movie(self, movie_id: str) -> None:
        movie = self.repo.get(movie_id)
        if not movie:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
        self.repo.delete(movie)
