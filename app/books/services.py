from app.auth.schemas import User
from app.books.schemas import Author
from app.common import db


async def add_author(author: Author, user: User):
    query = """
    INSERT INTO authors (first_name, surname, last_name, biography, birth_year, death_year, created_by, updated_by)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    RETURNING id;
"""
    return await db.fetch_one(query, author.first_name, author.surname, author.last_name,
                              author.biography, author.birth_year, author.death_year, user.id, user.id)


async def get_author_by_name(author: Author):
    query = "SELECT * FROM authors WHERE first_name = $1 AND surname = $2 AND (last_name = $3 OR (last_name IS NULL AND $3 IS NULL));"
    return await db.fetch_one(query, author.first_name, author.surname, author.last_name)

# async def add_book(book, )