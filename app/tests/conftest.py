import subprocess
import pytest

from app.constants import TEST_DATABASE_URL
from app.common import db

db.database_url = TEST_DATABASE_URL


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    yield
    subprocess.run(["alembic", "downgrade", "base"], check=True)
