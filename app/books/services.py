from app.books.repository import update_book_by_id, get_author_by_name, add_author, add_book_authors, add_book_genres, \
    clear_book_authors, clear_book_genres, add_book_record, delete_book_by_id, get_all_books_records, get_book_by_id
from app.books.schemas.book import Book
from app.books.schemas.genre import Genre
from app.books.utils import parse_authors
from app.common import Database


async def set_book_authors(author: str, book_id: int, user_id: int, db: Database):
    authors = parse_authors(author)
    author_records = [await get_author_by_name(author, db) or await add_author(author, user_id, db)
                      for author in authors]
    await add_book_authors(book_id, [author['id'] for author in author_records], db)
    return ','.join([' '.join([author['first_name'], author['surname']]) for author in author_records])


async def set_book_genres(genre_list: list[Genre], book_id: int, db: Database):
    return ','.join([genre['name'] for genre in await add_book_genres(book_id, [genre.name for genre in genre_list], db)])


async def update_book_instance(book_id: int, book_data: Book, user_id: int, db: Database):
    book_record = await update_book_by_id(book_id, book_data, user_id, db)
    response = dict(book_record)
    response['book_id'] = book_record['id']

    if book_data.author:
        await clear_book_authors(book_id, db)
        response['author'] = await set_book_authors(book_data.author, book_record['id'], user_id, db)

    if book_data.genre:
        await clear_book_genres(book_id, db)
        response['genre'] = await set_book_genres(book_data.genre_list, book_id, db)

    return response


async def add_book_instance(book_data: Book, user_id: int, db: Database):
    book_record = await add_book_record(book_data, user_id, db)
    response = dict(book_record)
    response['book_id'] = book_record['id']

    if book_data.author:
        response['author'] = await set_book_authors(book_data.author, book_record['id'], user_id, db)

    if book_data.genre:
        response['genre'] = await set_book_genres(book_data.genre_list, book_record['id'], db)

    return response


async def get_all_book_instances(db: Database, **kwargs):
    result = await get_all_books_records(db, **kwargs)
    return [dict(book) for book in result]


async def get_book_instance(book_id: int, db: Database):
    book = await get_book_by_id(book_id, db)
    return dict(book)


async def delete_book_instance(book_id: int, db: Database):
    result = await delete_book_by_id(book_id, db)
    return result
