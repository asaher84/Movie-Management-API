
from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel, Field, field_validator
from pydantic.generics import GenericModel

T = TypeVar("T")

class Paginated(GenericModel, Generic[T]):
    items: List[T]
    total: int
    limit: int
    offset: int

class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Movie title")
    director: Optional[str] = Field(None, max_length=100)
    releaseYear: Optional[int] = Field(None, ge=1888, le=2100, description="Year of release")
    genre: Optional[str] = Field(None, max_length=50)
    rating: Optional[float] = Field(None, ge=1, le=10, description="Rating from 1 to 10")

    @field_validator("title")
    @classmethod
    def title_strip(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("title cannot be blank")
        return s

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    director: Optional[str] = Field(None, max_length=100)
    releaseYear: Optional[int] = Field(None, ge=1888, le=2100)
    genre: Optional[str] = Field(None, max_length=50)
    rating: Optional[float] = Field(None, ge=1, le=10)

class MovieOut(MovieBase):
    id: str

    class Config:
        from_attributes = True
