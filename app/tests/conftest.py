import subprocess
from unittest.mock import AsyncMock

import pytest
from fastapi import Depends
from starlette.testclient import TestClient

from app.common import Database
from app.config import settings
from app.dependencies import get_db
from app.main import app
