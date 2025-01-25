from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class Book(BaseModel):
    title: str
    description: Optional[str] = None
    publication_year: int
    author: str
    genre: str

    @field_validator('publication_year')
    @classmethod
    def validate_year(cls, value: int):
        if not (1800 < value < datetime.now().year):
            raise ValueError('publication_year must be between 1800 and current')
        return value


class AuthorRelatedBook(Book):
    author: int


class Author(BaseModel):
    first_name: str
    surname: str
    last_name: Optional[str] = None
    biography: Optional[str] = None
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
