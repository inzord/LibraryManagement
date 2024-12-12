from datetime import date

from sqlalchemy import Integer, ForeignKey, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base


class Borrow(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("book.id"),
                                         nullable=False)
    reader_name: Mapped[str] = mapped_column(String, nullable=False)
    borrow_date: Mapped[date] = mapped_column(Date, nullable=False)
    return_date: Mapped[date] = mapped_column(Date, nullable=True)

    book: Mapped["Book"] = relationship("Book", back_populates="borrows")

    def __repr__(self) -> str:
        return f"Borrow(id={self.id!r}, book_id={self.book_id!r}, reader_name={self.reader_name!r})"
