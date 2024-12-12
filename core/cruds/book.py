from sqlalchemy.orm import Session
from typing import Type, Optional
from core.models.book import Book as BookModel, Book
from core.schemas.book import BookCreate, BookUpdate


class BookCRUD:
    """
    Класс для управления данными книг в базе данных.
    """

    @staticmethod
    def create_book(db: Session, book: BookCreate) -> BookModel:
        """
        Создает новую книгу в базе данных.

        Args:
            db (Session): Сессия базы данных.
            book (BookCreate): Данные новой книги.

        Returns:
            BookModel: Объект созданной книги.
        """
        db_book = BookModel(**book.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def get_book(db: Session, book_id: int) -> Type[Book] | None:
        """
        Возвращает книгу по ее идентификатору.

        Args:
            db (Session): Сессия базы данных.
            book_id (int): Идентификатор книги.

        Returns:
            Type[Book] | None: Объект книги или None, если книга не найдена.
        """
        return db.query(BookModel).filter(BookModel.id == book_id).first()

    @staticmethod
    def get_books(db: Session, skip: int = 0, limit: int = 10) -> list[Type[Book]]:
        """
        Возвращает список книг с возможностью пагинации.

        Args:
            db (Session): Сессия базы данных.
            skip (int, optional): Количество книг, которые нужно пропустить. Defaults to 0.
            limit (int, optional): Количество книг, которые нужно вернуть. Defaults to 10.

        Returns:
            list[Type[Book]]: Список книг.
        """
        return db.query(BookModel).offset(skip).limit(limit).all()

    @staticmethod
    def update_book(db: Session, book_id: int, book: BookUpdate) -> Type[Book] | None:
        """
        Обновляет данные книги.

        Args:
            db (Session): Сессия базы данных.
            book_id (int): Идентификатор книги.
            book (BookUpdate): Данные для обновления.

        Returns:
            Type[Book] | None: Объект обновленной книги или None, если книга не найдена.
        """
        db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
        if db_book:
            for key, value in book.dict(exclude_unset=True).items():
                setattr(db_book, key, value)
            db.commit()
            db.refresh(db_book)
        return db_book

    @staticmethod
    def delete_book(db: Session, book_id: int) -> Optional[Type[Book]] | None:
        """
        Удаляет книгу из базы данных.

        Args:
            db (Session): Сессия базы данных.
            book_id (int): Идентификатор книги.

        Returns:
            Optional[Type[Book]] | None: Объект удаленной книги или None, если книга не найдена.
        """
        db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
        if db_book:
            # Удаляем все записи о выдаче книги
            for borrow in db_book.borrows:
                db.delete(borrow)
            db.commit()
            # Теперь удаляем книгу
            db.delete(db_book)
            db.commit()
        return db_book
