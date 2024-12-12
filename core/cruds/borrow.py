from sqlalchemy.orm import Session
from typing import Type
from core.models.borrow import Borrow as BorrowModel, Borrow
from core.schemas.borrow import BorrowCreate, BorrowUpdate


class BorrowCRUD:
    """
    Класс для управления данными о выдаче книг в базе данных.
    """

    @staticmethod
    def create_borrow(db: Session, borrow: BorrowCreate) -> BorrowModel:
        """
        Создает новую запись о выдаче книги в базе данных.

        Args:
            db (Session): Сессия базы данных.
            borrow (BorrowCreate): Данные новой записи о выдаче книги.

        Returns:
            BorrowModel: Объект созданной записи о выдаче книги.
        """
        db_borrow = BorrowModel(**borrow.model_dump())
        db.add(db_borrow)
        db.commit()
        db.refresh(db_borrow)
        return db_borrow

    @staticmethod
    def get_borrow(db: Session, borrow_id: int) -> Type[Borrow] | None:
        """
        Возвращает запись о выдаче книги по ее идентификатору.

        Args:
            db (Session): Сессия базы данных.
            borrow_id (int): Идентификатор записи о выдаче книги.

        Returns:
            Type[Borrow] | None: Объект записи о выдаче книги или None, если запись не найдена.
        """
        return db.query(BorrowModel).filter(BorrowModel.id == borrow_id).first()

    @staticmethod
    def get_borrows(db: Session, skip: int = 0, limit: int = 10) -> list[Type[Borrow]]:
        """
        Возвращает список записей о выдаче книг с возможностью пагинации.

        Args:
            db (Session): Сессия базы данных.
            skip (int, optional): Количество записей о выдаче книг, которые нужно пропустить. Defaults to 0.
            limit (int, optional): Количество записей о выдаче книг, которые нужно вернуть. Defaults to 10.

        Returns:
            list[Type[Borrow]]: Список записей о выдаче книг.
        """
        return db.query(BorrowModel).offset(skip).limit(limit).all()

    @staticmethod
    def update_borrow(db: Session, borrow_id: int, borrow: BorrowUpdate) -> Type[Borrow] | None:
        """
        Обновляет данные записи о выдаче книги.

        Args:
            db (Session): Сессия базы данных.
            borrow_id (int): Идентификатор записи о выдаче книги.
            borrow (BorrowUpdate): Данные для обновления.

        Returns:
            Type[Borrow] | None: Объект обновленной записи о выдаче книги или None, если запись не найдена.
        """
        db_borrow = db.query(BorrowModel).filter(BorrowModel.id == borrow_id).first()
        if db_borrow:
            for key, value in borrow.dict(exclude_unset=True).items():
                setattr(db_borrow, key, value)
            db.commit()
            db.refresh(db_borrow)
        return db_borrow
