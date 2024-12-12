from typing import List

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base


class Book(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    author_id: Mapped[int] = mapped_column(Integer,
                                           ForeignKey("author.id"), nullable=True)
    available_copies: Mapped[int] = mapped_column(Integer, nullable=False)

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    borrows: Mapped[List["Borrow"]] = relationship("Borrow", back_populates="book")

    def __repr__(self) -> str:
        return f"Book(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})"
