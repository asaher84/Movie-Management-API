
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.dao.db import SessionLocal, engine, Base
from app.dao.movie_repository import MovieRepository
from app.services.movie_service import MovieService
from app.schemas.movie import MovieCreate, MovieUpdate, MovieOut, Paginated
from app.core.config import settings

router = APIRouter(prefix="/movies", tags=["Movies"])

# Ensure DB tables exist at import-time for simplicity
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_service(db: Session = Depends(get_db)) -> MovieService:
    return MovieService(MovieRepository(db))

@router.get("", response_model=Paginated[MovieOut])
def list_movies(
    limit: int = Query(default=settings.page_limit_default, ge=1, le=settings.page_limit_max),
    offset: int = Query(default=0, ge=0),
    service: MovieService = Depends(get_service),
):
    items, total = service.list_movies(limit=limit, offset=offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}

@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: str, service: MovieService = Depends(get_service)):
    return service.get_movie(movie_id)

@router.post("", response_model=MovieOut, status_code=201)
def create_movie(payload: MovieCreate, service: MovieService = Depends(get_service)):
    return service.create_movie(payload)

@router.put("/{movie_id}", response_model=MovieOut)
def update_movie(movie_id: str, payload: MovieUpdate, service: MovieService = Depends(get_service)):
    return service.update_movie(movie_id, payload)

@router.delete("/{movie_id}", status_code=204)
def delete_movie(movie_id: str, service: MovieService = Depends(get_service)):
    service.delete_movie(movie_id)
    return None
