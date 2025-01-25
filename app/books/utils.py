import re

from app.books.schemas.author import Author


def parse_authors(authors_string: str) -> list[Author]:
    authors = re.split(r'\s+and\s+|\s*,\s*', authors_string.strip())

    parsed_authors = []
    for author in authors:
        parts = author.split()
        if len(parts) >= 2:
            first_name = parts[0]
            last_name = parts[-1] if len(parts) > 2 else None
            surname = parts[-2] if len(parts) > 2 else parts[-1]
            parsed_authors.append(Author(first_name=first_name, last_name=last_name, surname=surname))

    return parsed_authors


def parse_genres(genres_string: str) -> list[str]:
    genres = re.split(r'\s*,\s*|\s+and\s+', genres_string.strip())

    return [genre.strip() for genre in genres if genre.strip()]
