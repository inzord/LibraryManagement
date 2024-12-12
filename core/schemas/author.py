from pydantic import BaseModel
from datetime import date


class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: date


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True
