import asyncio

from app.auth.schemas import User
from app.books.schemas.author import Author
from app.books.schemas.book import Book
from app.common import db


async def add_author(author: Author, user: User):
    query = """
    INSERT INTO authors (first_name, surname, last_name, biography, birth_year, death_year, created_by, updated_by)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    RETURNING *;
"""
    return await db.fetch_one(query, author.first_name, author.surname, author.last_name,
                              author.biography, author.birth_year, author.death_year, user.id, user.id)


async def get_author_by_name(author: Author):
    query = "SELECT * FROM authors WHERE first_name = $1 AND surname = $2 AND (last_name = $3 OR (last_name IS NULL AND $3 IS NULL));"
    return await db.fetch_one(query, author.first_name, author.surname, author.last_name)


async def add_book_record(book: Book, user: User):
    query = """INSERT INTO books (
    title, 
    description, 
    publication_year, 
    created_by, 
    updated_by
) VALUES (
    $1,     -- title
    $2,     -- description
    $3,     -- publication_year
    $4,     -- created_by
    $5      -- updated_by
)
RETURNING *;
"""
    return await db.fetch_one(query, book.title, book.description, book.publication_year, user.id, user.id)


async def add_book_authors(book_id: int, authors: list[int]):
    query = "INSERT INTO book_authors (book_id, author_id) VALUES ($1, $2);"

    tasks = [db.execute(query, book_id, author_id) for author_id in authors]
    await asyncio.gather(*tasks)


async def add_book_genres(book_id: int, genres: list[str]):
    query = """
        WITH selected_genres AS (
            SELECT id, name
            FROM genres
            WHERE name = ANY($1)
        ),
        inserted_relationships AS (
            INSERT INTO book_genres (book_id, genre_id)
            SELECT $2, id
            FROM selected_genres
            ON CONFLICT DO NOTHING
            RETURNING book_id, genre_id
        )
        SELECT ir.book_id, ir.genre_id, sg.name
        FROM inserted_relationships ir
        JOIN selected_genres sg ON ir.genre_id = sg.id;
    """
    result = await db.fetch_all(query, genres, book_id)
    return result


async def get_all_books_records():
    query = """
       SELECT 
    b.id AS book_id,
    b.title,
    b.description,
    b.publication_year,
    -- Concatenate authors' full names into a single string
    STRING_AGG(DISTINCT a.first_name || ' ' || a.surname, ', ') AS author,
    -- Concatenate genres into a single string
    STRING_AGG(DISTINCT g.name, ', ') AS genre
FROM 
    books b
-- Join with authors
JOIN 
    book_authors ba ON b.id = ba.book_id
JOIN 
    authors a ON ba.author_id = a.id
-- Join with genres
JOIN 
    book_genres bg ON b.id = bg.book_id
JOIN 
    genres g ON bg.genre_id = g.id
GROUP BY 
    b.id, b.title, b.description, b.publication_year;

"""
    return await db.fetch_all(query)
