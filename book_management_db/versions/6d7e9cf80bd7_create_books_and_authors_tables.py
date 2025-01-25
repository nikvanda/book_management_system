"""create books and authors tables

Revision ID: 6d7e9cf80bd7
Revises: 
Create Date: 2025-01-24 23:25:03.470005

"""

from alembic import op


revision: str = '6d7e9cf80bd7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        registered_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP WITH TIME ZONE
    );
    """)

    op.execute("""
    CREATE TABLE books (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        publication_year INTEGER CHECK (publication_year > 1800),
        created_by INTEGER NOT NULL,
        updated_by INTEGER NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES users(id),
        FOREIGN KEY (updated_by) REFERENCES users(id)
    );
    """)

    op.execute("""
    CREATE TABLE genres (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL
    );
    """)

    op.execute("""
    CREATE TABLE book_genres (
        book_id INTEGER NOT NULL,
        genre_id INTEGER NOT NULL,
        PRIMARY KEY (book_id, genre_id),
        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
        FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
    );
    """)

    op.execute("""
    CREATE TABLE authors (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        surname VARCHAR(100) NOT NULL,
        last_name VARCHAR(100),
        biography TEXT,
        birth_year INTEGER,
        death_year INTEGER,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        created_by INTEGER NOT NULL,
        updated_by INTEGER NOT NULL,
        FOREIGN KEY (created_by) REFERENCES users(id),
        FOREIGN KEY (updated_by) REFERENCES users(id)
    );
    """)

    op.execute("""
    CREATE TABLE book_authors (
        book_id INTEGER NOT NULL,
        author_id INTEGER NOT NULL,
        PRIMARY KEY (book_id, author_id),
        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
        FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
    );
    """)


def downgrade():
    op.execute("DROP TABLE IF EXISTS book_authors;")
    op.execute("DROP TABLE IF EXISTS authors;")
    op.execute("DROP TABLE IF EXISTS book_genres;")
    op.execute("DROP TABLE IF EXISTS genres;")
    op.execute("DROP TABLE IF EXISTS books;")
    op.execute("DROP TABLE IF EXISTS users;")