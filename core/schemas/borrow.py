from typing import Optional

from pydantic import BaseModel, field_validator
from datetime import date


class BorrowBase(BaseModel):
    book_id: int
    reader_name: str
    borrow_date: date
    return_date: Optional[date] = None

    @field_validator('return_date', mode='before')
    def format_return_date(cls, v):
        if isinstance(v, date):
            return v.isoformat()  # Преобразуем дату в строку формата 'YYYY-MM-DD'
        return v


class BorrowCreate(BorrowBase):
    pass


class BorrowUpdate(BorrowBase):
    pass


class Borrow(BorrowBase):
    id: int

    class Config:
        from_attributes = True
