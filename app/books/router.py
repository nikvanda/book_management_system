import csv
import json
from io import StringIO
from typing import Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from pydantic import ValidationError
from starlette.responses import JSONResponse

from .schemas.book import Book, BookResponse
from .services import add_book_instance, update_book_instance, delete_book_instance, get_all_book_instances, \
    get_book_instance
from ..dependencies import CurrentUser, DB

router = APIRouter(prefix='/books')


@router.post('/', response_model=BookResponse)
async def add_book(book: Book, current_user: CurrentUser, db: DB):
    try:
        response = await add_book_instance(book, current_user.id, db)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error adding book: {str(e)}")


@router.get('/', response_model=list[BookResponse])
async def get_all_books(db: DB,
                        title: Optional[str] = Query(None, description="Filter by title (partial match)"),
                        author: Optional[str] = Query(None, description="Filter by author (partial match)"),
                        genre: Optional[str] = Query(None, description="Filter by genre (exact match)"),
                        year_from: Optional[int] = Query(None, description="Filter by publication year (from)"),
                        year_to: Optional[int] = Query(None, description="Filter by publication year (to)"),
                        page: int = Query(1, ge=1, description="Page number (1-indexed)"),
                        page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
                        sort_by: str = Query("title", description="Column to sort by (title or year)"),
                        sort_order: str = Query("asc", description="Sort order ('asc' or 'desc')")):
    valid_sort_columns = {"title", "year", "author", "genre"}
    if sort_by not in valid_sort_columns:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by value. Must be one of {valid_sort_columns}")

    if sort_order not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail="Invalid sort_order value. Must be 'asc' or 'desc'")

    start_item = (page - 1) * page_size

    try:
        books = await get_all_book_instances(db, title=title, author=author, genre=genre,
                                             year_from=year_from, year_to=year_to, page_size=page_size,
                                             start_item=start_item, sort_by=sort_by, sort_order=sort_order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching books: {str(e)}")

    if books:
        return books
    return JSONResponse(status_code=404, content='No data.')


@router.get('/{book_id}', response_model=BookResponse)
async def get_book(book_id: int, db: DB):
    try:
        book = await get_book_instance(book_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching book with ID {book_id}: {str(e)}")

    if book:
        return book
    return JSONResponse(
        status_code=404,
        content={"detail": "Book not found", "book_id": book_id})


@router.delete('/{book_id}')
async def delete_book(book_id: int, current_user: CurrentUser, db: DB):
    try:
        response = await delete_book_instance(book_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting book.")

    if response:
        return JSONResponse(status_code=204, content='Book was deleted.')
    else:
        return JSONResponse(status_code=404, content=f'No book found with ID {book_id}.')


@router.patch('/{book_id}', response_model=BookResponse)
async def update_book(book_id: int, book: Book, current_user: CurrentUser, db: DB):
    try:
        updated_book = await update_book_instance(book_id, book, current_user.id, db)
        return updated_book
    except ValidationError as e:
        msg = 'Input data is invalid'
        if e.title == 'Genre':
            msg = 'Genre is not allowed'
        return JSONResponse(status_code=400, content=msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating book with ID {book_id}: {str(e)}")


@router.post('/import')
async def import_books_from_file(current_user: CurrentUser, db: DB, file: UploadFile = File(...)):
    try:
        if file.content_type == "application/json":
            contents = await file.read()
            try:
                books_data = json.loads(contents.decode())
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON file format")
            for book in books_data:
                book_obj = Book(**book)
                await add_book_instance(book_obj, current_user.id, db)
            return JSONResponse(status_code=200, content='Data was uploaded.')

        elif file.content_type == "text/csv":
            contents = await file.read()
            try:
                decoded = contents.decode()
                csv_reader = csv.DictReader(StringIO(decoded))
            except Exception as e:
                raise HTTPException(status_code=400, detail="Error reading CSV file")

            for row in csv_reader:
                try:
                    book_obj = Book(**row)
                    await add_book_instance(book_obj, current_user.id, db)
                except Exception as e:
                    raise HTTPException(status_code=400, detail=f"Error processing book: {e}")

            return JSONResponse(status_code=200, content='Data was uploaded.')

        else:
            raise HTTPException(status_code=400, detail="Provided file type is not supported.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing books: {str(e)}")
