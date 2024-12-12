from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.cruds.book import BookCRUD
from core.cruds.borrow import BorrowCRUD
from core.schemas.author import Author, AuthorCreate, AuthorUpdate
from core.cruds.author import AuthorCRUD
from core.schemas.book import Book, BookCreate, BookUpdate
from core.schemas.borrow import Borrow, BorrowCreate
from db.database import create_db, SessionLocal

app = FastAPI()

# Создание базы данных
create_db()


# Dependency для получения сессии базы данных
def get_db():
    with SessionLocal() as db:
        yield db


# Эндпоинты для авторов
@app.post("/authors/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return AuthorCRUD.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[Author])
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return AuthorCRUD.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = AuthorCRUD.get_author(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.put("/authors/{author_id}", response_model=Author)
def update_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    updated_author = AuthorCRUD.update_author(db=db, author_id=author_id, author=author)
    if updated_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated_author


@app.delete("/authors/{author_id}", response_model=Author)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    deleted_author = AuthorCRUD.delete_author(db=db, author_id=author_id)
    if deleted_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return deleted_author


# Эндпоинты для книг
@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return BookCRUD.create_book(db=db, book=book)


@app.get("/books/", response_model=List[Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return BookCRUD.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = BookCRUD.get_book(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    updated_book = BookCRUD.update_book(db=db, book_id=book_id, book=book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_to_delete = BookCRUD.get_book(db=db, book_id=book_id)

    if book_to_delete is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Удалите книгу из базы данных
    BookCRUD.delete_book(db=db, book_id=book_id)

    # Преобразуйте книгу в Pydantic модель и верните ее
    return Book.from_orm(book_to_delete)


# Эндпоинты для выдач
@app.post("/borrows/", response_model=Borrow)
def create_borrow(borrow: BorrowCreate, db: Session = Depends(get_db)):
    book = BookCRUD.get_book(db=db, book_id=borrow.book_id)
    if book is None or book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book is not available for borrowing")

    # Уменьшаем количество доступных экземпляров
    book.available_copies -= 1
    db.commit()

    return BorrowCRUD.create_borrow(db=db, borrow=borrow)


@app.get("/borrows/", response_model=List[Borrow])
def get_borrows(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return BorrowCRUD.get_borrows(db=db, skip=skip, limit=limit)


@app.get("/borrows/{borrow_id}", response_model=Borrow)
def get_borrow(borrow_id: int, db: Session = Depends(get_db)):
    borrow = BorrowCRUD.get_borrow(db=db, borrow_id=borrow_id)
    if borrow is None:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    return borrow


@app.patch("/borrows/{borrow_id}/return", response_model=Borrow)
def return_borrow(borrow_id: int, return_date: str, db: Session = Depends(get_db)):
    # Получаем запись о займе
    borrow = BorrowCRUD.get_borrow(db=db, borrow_id=borrow_id)
    if borrow is None:
        raise HTTPException(status_code=404, detail="Borrow record not found")

    # Преобразуем строку return_date в объект date
    try:
        return_date_obj = datetime.strptime(return_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'.")

    # Увеличиваем количество доступных экземпляров
    book = BookCRUD.get_book(db=db, book_id=borrow.book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book.available_copies += 1

    # Обновляем дату возврата
    borrow.return_date = return_date_obj
    db.commit()
    db.refresh(borrow)

    return borrow
