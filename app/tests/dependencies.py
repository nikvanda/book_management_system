from typing import Annotated

from fastapi import Depends

from app.common import db, Database


def get_test_db() -> Database:
    return db


def get_db_dependency(database: Database = Depends(get_test_db)) -> Database:
    return database


DB_TEST = Annotated[Database, Depends(get_db_dependency)]
