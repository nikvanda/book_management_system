from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator, computed_field

from app.books.schemas.genre import Genre
from app.books.utils import parse_genres


class BookResponse(BaseModel):
    book_id: int = None
    title: str
    description: Optional[str] = None
    publication_year: int
    author: str
    genre: str


class Book(BookResponse):
    @field_validator('publication_year')
    @classmethod
    def validate_year(cls, value: int):
        if not (1800 < value < datetime.now().year):
            raise ValueError('publication_year must be between 1800 and current')
        return value

    @computed_field
    def genre_list(self) -> list[Genre]:
        return [Genre(name=genre) for genre in parse_genres(self.genre)]
