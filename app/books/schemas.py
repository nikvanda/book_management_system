from typing import Optional

from pydantic import BaseModel


class Book(BaseModel):
    title: str
    description: Optional[str]
    publication_year: int
    author: str
    genre: str


class AuthorRelatedBook(Book):
    author: int


class Author(BaseModel):
    first_name: str
    surname: str
    last_name: Optional[str] = None
    biography: Optional[str] = None
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
