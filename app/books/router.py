from typing import Annotated

from fastapi import APIRouter, Depends

from .schemas.book import Book, BookResponse
from .services import add_author, get_author_by_name, add_book_record, add_book_authors, add_book_genres, \
    get_all_books_records, get_book_by_id
from app.auth.schemas import User
from app.auth.services import get_current_active_user
from .utils import parse_authors

router = APIRouter(prefix='/books')


@router.post('/', response_model=BookResponse)
async def add_book(book: Book, current_user: Annotated[User, Depends(get_current_active_user)]):
    authors = parse_authors(book.author)
    author_records = [await get_author_by_name(author) or await add_author(author, current_user)
                      for author in authors]

    created_book = await add_book_record(book, current_user)
    genres = [genre['name'] for genre in await add_book_genres(created_book['id'],
                                                               [genre.name for genre in book.genre_list])]

    await add_book_authors(created_book['id'], [author['id'] for author in author_records])

    response = BookResponse(book_id=created_book['id'],
                            title=created_book['title'],
                            description=created_book['description'],
                            publication_year=created_book['publication_year'],
                            author=','.join(
                                [' '.join([author['first_name'], author['surname']]) for author in author_records]),
                            genre=','.join(genres)
                            )
    return response


@router.get('/', response_model=list[BookResponse])
async def get_all_books(): # todo: does not return book if author is empty. need to check the same for genre
    return [dict(book) for book in await get_all_books_records()]


@router.get('/{book_id}', response_model=BookResponse) #todo: add detail response
async def get_book(book_id: int):
    book = await get_book_by_id(book_id)
    return dict(book)
