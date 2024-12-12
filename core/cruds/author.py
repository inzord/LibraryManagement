from sqlalchemy.orm import Session
from typing import Type, Optional
from core.models.author import Author as AuthorModel, Author

from core.schemas.author import AuthorCreate, AuthorUpdate


class AuthorCRUD:
    """
    Класс для управления данными авторов в базе данных.
    """

    @staticmethod
    def create_author(db: Session, author: AuthorCreate) -> AuthorModel:
        """
        Создает нового автора в базе данных.

        Args:
            db (Session): Сессия базы данных.
            author (AuthorCreate): Данные нового автора.

        Returns:
            AuthorModel: Объект созданного автора.
        """
        db_author = AuthorModel(**author.model_dump())
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return db_author

    @staticmethod
    def get_author(db: Session, author_id: int) -> Type[Author] | None:
        """
        Возвращает автора по его идентификатору.

        Args:
            db (Session): Сессия базы данных.
            author_id (int): Идентификатор автора.

        Returns:
            Type[Author] | None: Объект автора или None, если автор не найден.
        """
        return db.query(AuthorModel).filter(AuthorModel.id == author_id).first()

    @staticmethod
    def get_authors(db: Session, skip: int = 0, limit: int = 10) -> list[Type[Author]]:
        """
        Возвращает список авторов с возможностью пагинации.

        Args:
            db (Session): Сессия базы данных.
            skip (int, optional): Количество авторов, которые нужно пропустить. Defaults to 0.
            limit (int, optional): Количество авторов, которые нужно вернуть. Defaults to 10.

        Returns:
            list[Type[Author]]: Список авторов.
        """
        return db.query(AuthorModel).offset(skip).limit(limit).all()

    @staticmethod
    def update_author(db: Session, author_id: int, author: AuthorUpdate) -> Type[Author] | None:
        """
        Обновляет данные автора.

        Args:
            db (Session): Сессия базы данных.
            author_id (int): Идентификатор автора.
            author (AuthorUpdate): Данные для обновления.

        Returns:
            Type[Author] | None: Объект обновленного автора или None, если автор не найден.
        """
        db_author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
        if db_author:
            for key, value in author.model_dump(exclude_unset=True).items():
                setattr(db_author, key, value)
            db.commit()
            db.refresh(db_author)
        return db_author

    @staticmethod
    def delete_author(db: Session, author_id: int) -> Optional[Type[AuthorModel]]:
        """
        Удаляет автора из базы данных.

        Args:
            db (Session): Сессия базы данных.
            author_id (int): Идентификатор автора.

        Returns:
            Optional[Type[AuthorModel]]: Объект удаленного автора или None, если автор не найден.
        """
        db_author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
        if db_author:
            # Устанавливаем author_id в None для всех книг, связанных с автором
            for book in db_author.books:
                book.author_id = None  # Или можно переназначить на другого автора
            db.commit()  # Сохраняем изменения в базе данных

            # Теперь удаляем автора
            db.delete(db_author)
            db.commit()  # Сохраняем изменения в базе данных
        return db_author
