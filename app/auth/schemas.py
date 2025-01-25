from pydantic import BaseModel, UUID4


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: UUID4
    username: str
    password: str
    registered_at: int
    last_login: int


