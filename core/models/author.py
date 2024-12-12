from datetime import date
from typing import List

from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base  # Импортируйте базовый класс


class Author(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)

    books: Mapped[List["Book"]] = relationship("Book", back_populates="author")

    def __repr__(self) -> str:
        return f"Author(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"
