import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models.author import Author
from core.models.base import Base
from core.models.book import Book
from core.models.borrow import Borrow
from sqlalchemy.orm import Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./library.db")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db():
    if not os.path.exists("library.db"):
        # Создание всех таблиц
        Base.metadata.create_all(bind=engine)

        # Заполнение тестовыми данными
        db: Session = SessionLocal()
        try:
            # Добавление авторов
            authors = [
                Author(first_name="Leo", last_name="Tolstoy",
                       birth_date=datetime.strptime("1828-09-09", '%Y-%m-%d').date()),
                Author(first_name="Fyodor", last_name="Dostoevsky",
                       birth_date=datetime.strptime("1821-11-11", '%Y-%m-%d').date()),
                Author(first_name="Anton", last_name="Chekhov",
                       birth_date=datetime.strptime("1860-01-29", '%Y-%m-%d').date()),
                Author(first_name="Virginia", last_name="Woolf",
                       birth_date=datetime.strptime("1882-01-25", '%Y-%m-%d').date()),
                Author(first_name="Gabriel", last_name="Garcia Marquez",
                       birth_date=datetime.strptime("1927-03-06", '%Y-%m-%d').date()),
            ]
            db.add_all(authors)
            db.commit()

            # Добавление книг
            books = [
                Book(title="War and Peace", description="A historical novel by Leo Tolstoy.", author_id=1,
                     available_copies=3),
                Book(title="Crime and Punishment", description="A novel by Fyodor Dostoevsky.", author_id=2,
                     available_copies=2),
                Book(title="The Cherry Orchard", description="A play by Anton Chekhov.", author_id=3,
                     available_copies=5),
                Book(title="Mrs. Dalloway", description="A novel by Virginia Woolf.", author_id=4, available_copies=4),
                Book(title="One Hundred Years of Solitude", description="A novel by Gabriel Garcia Marquez.",
                     author_id=5,
                     available_copies=1),
            ]
            db.add_all(books)
            db.commit()

            # Добавление записей о выдаче
            borrows = [
                Borrow(book_id=1, reader_name="Alice", borrow_date=datetime.strptime("2023-01-01", '%Y-%m-%d').date()),
                Borrow(book_id=2, reader_name="Bob", borrow_date=datetime.strptime("2023-01-05", '%Y-%m-%d').date()),
                Borrow(book_id=3, reader_name="Charlie",
                       borrow_date=datetime.strptime("2023-01-10", '%Y-%m-%d').date()),
                Borrow(book_id=4, reader_name="Diana", borrow_date=datetime.strptime("2023-01-15", '%Y-%m-%d').date()),
                Borrow(book_id=5, reader_name="Eve", borrow_date=datetime.strptime("2023-01-20", '%Y-%m-%d').date()),
            ]
            db.add_all(borrows)
            db.commit()

        finally:
            db.close()
