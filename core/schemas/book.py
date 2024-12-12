from pydantic import BaseModel
from typing import List, Optional

from core.models.borrow import Borrow


class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    author_id: int
    available_copies: int


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        from_attributes = True
