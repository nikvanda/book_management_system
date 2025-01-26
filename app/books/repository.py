import asyncio

from app.books.schemas.author import Author
from app.books.schemas.book import Book
from app.common import db


async def add_author(author: Author, user_id: int):
    query = """
    INSERT INTO authors (first_name, surname, last_name, biography, birth_year, death_year, created_by, updated_by)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    RETURNING *;
"""
    return await db.fetch_one(query, author.first_name, author.surname, author.last_name,
                              author.biography, author.birth_year, author.death_year, user_id, user_id)


async def get_author_by_name(author: Author):
    query = "SELECT * FROM authors WHERE first_name = $1 AND surname = $2 AND (last_name = $3 OR (last_name IS NULL AND $3 IS NULL));"
    return await db.fetch_one(query, author.first_name, author.surname, author.last_name)


async def add_book_record(book: Book, user_id):
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
    return await db.fetch_one(query, book.title, book.description, book.publication_year, user_id, user_id)


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
    return await db.fetch_all(query, genres, book_id)


async def get_all_books_records(title: str = None, author: str = None, genre: str = None,
                                year_from: int = None, year_to: int = None, start_item: int = 0,
                                page_size: int = 10, sort_by: str = 'title', sort_order: str = 'asc'):
    query = f"""
     SELECT 
    b.id AS book_id,
    b.title,
    b.description,
    b.publication_year,
    -- Concatenate authors' full names into a single string, handle NULLs
    COALESCE(STRING_AGG(DISTINCT a.first_name || ' ' || a.surname, ', '), 'No authors') AS author,
    -- Concatenate genres into a single string, handle NULLs
    COALESCE(STRING_AGG(DISTINCT g.name, ', '), 'No genres') AS genre
FROM 
    books b
-- Left join with authors
LEFT JOIN 
    book_authors ba ON b.id = ba.book_id
LEFT JOIN 
    authors a ON ba.author_id = a.id
-- Left join with genres
LEFT JOIN 
    book_genres bg ON b.id = bg.book_id
LEFT JOIN 
    genres g ON bg.genre_id = g.id
WHERE
    -- Filter by title if provided (use ILIKE for case-insensitive matching)
    (b.title ILIKE COALESCE($1, b.title))
    -- Filter by author if provided (concatenate authors' names and match)
    AND (a.first_name || ' ' || a.surname ILIKE COALESCE($2, a.first_name || ' ' || a.surname))
    -- Filter by genre if provided
    AND (g.name ILIKE COALESCE($3, g.name))
    -- Filter by publication year range if provided
    AND (b.publication_year BETWEEN COALESCE($4, b.publication_year) AND COALESCE($5, b.publication_year))
GROUP BY 
    b.id, b.title, b.description, b.publication_year
-- Sorting
ORDER BY 
    CASE 
        WHEN $6 = 'title' THEN b.title
        WHEN $6 = 'publication_year' THEN b.publication_year::TEXT -- Cast to TEXT
        ELSE b.title -- Default sort by title
    END 
    {sort_order.upper()} -- Sort direction (ASC or DESC)
-- Pagination
LIMIT $7 OFFSET $8;
"""
    return await db.fetch_all(query, title, author, genre, year_from, year_to, sort_by, page_size, start_item)


async def get_book_by_id(book_id: int):
    query = """
       SELECT 
    b.id AS book_id,
    b.title,
    b.description,
    b.publication_year,
    -- Concatenate authors' full names into a single string, handle NULLs
    COALESCE(STRING_AGG(DISTINCT a.first_name || ' ' || a.surname, ', '), 'No authors') AS author,
    -- Concatenate genres into a single string, handle NULLs
    COALESCE(STRING_AGG(DISTINCT g.name, ', '), 'No genres') AS genre
FROM 
    books b
-- Left join with authors
LEFT JOIN 
    book_authors ba ON b.id = ba.book_id
LEFT JOIN 
    authors a ON ba.author_id = a.id
-- Left join with genres
LEFT JOIN 
    book_genres bg ON b.id = bg.book_id
LEFT JOIN 
    genres g ON bg.genre_id = g.id
-- Filter by book_id
WHERE 
    b.id = $1
GROUP BY 
    b.id, b.title, b.description, b.publication_year;
"""
    return await db.fetch_one(query, book_id)


async def delete_book_by_id(book_id: int):
    query = """DELETE FROM books WHERE id = $1 RETURNING id;"""
    return await db.fetch_one(query, book_id)


async def clear_book_authors(book_id: int):
    query = """DELETE FROM book_authors WHERE book_id = $1;"""
    await db.execute(query, book_id)


async def clear_book_genres(book_id: int):
    query = """DELETE FROM book_genres WHERE book_id = $1;"""
    await db.execute(query, book_id)


async def update_book_by_id(book_id: int, book_data: Book, user_id: int):
    query = """UPDATE books
SET
    title = COALESCE($1, title),
    description = COALESCE($2, description),
    publication_year = COALESCE($3, publication_year),
    updated_by = $4,
    updated_at = CURRENT_TIMESTAMP
WHERE id = $5
RETURNING *;
    """
    return await db.fetch_one(query, book_data.title, book_data.description,
                              book_data.publication_year, user_id, book_id)
