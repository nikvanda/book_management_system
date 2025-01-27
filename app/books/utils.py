import re
from app.books.schemas.author import Author


def parse_authors(authors_string: str) -> list[Author]:
    try:
        if not authors_string or not isinstance(authors_string, str):
            raise ValueError("The input string is invalid or empty.")

        authors = re.split(r'\s+and\s+|\s*,\s*', authors_string.strip())

        parsed_authors = []
        for author in authors:
            parts = author.split()

            if len(parts) < 2:
                raise ValueError(f"Invalid author format: '{author}'")

            first_name = parts[0]
            last_name = parts[-1] if len(parts) > 2 else None
            surname = parts[-2] if len(parts) > 2 else parts[-1]

            parsed_authors.append(Author(first_name=first_name, last_name=last_name, surname=surname))

        return parsed_authors
    except Exception as e:
        print(f"Error in parse_authors: {e}")
        raise ValueError(f"Failed to parse authors from the string: {authors_string}")


def parse_genres(genres_string: str) -> list[str]:
    try:
        if not genres_string or not isinstance(genres_string, str):
            raise ValueError("The input string for genres is invalid or empty.")

        genres = re.split(r'\s*,\s*|\s+and\s+', genres_string.strip())

        return [genre.strip() for genre in genres if genre.strip()]
    except Exception as e:
        print(f"Error in parse_genres: {e}")
        raise ValueError(f"Failed to parse genres from the string: {genres_string}")
