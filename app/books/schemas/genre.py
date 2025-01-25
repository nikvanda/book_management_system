from typing import Any
from typing_extensions import Self

from pydantic import BaseModel, field_validator

from app.constants import GENRES


class Genre(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def validate(cls, value: Any) -> Self:
        if value not in GENRES:
            raise ValueError(f'f{value} is not allowed')
        return value
