import os
import pytest
from fastapi.testclient import TestClient
from db.database import create_db, SessionLocal
from main import app

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    create_db()
    yield


@pytest.fixture
def db_session():
    with SessionLocal() as db:
        yield db


def test_create_author(db_session):
    response = client.post("/authors/", json={"first_name": "Test", "last_name": "Author", "birth_date": "1927-03-06"})
    assert response.status_code == 200
    assert response.json()["first_name"] == "Test"


def test_get_authors(db_session):
    response = client.get("/authors/", params={"skip": 0, "limit": 10})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_author(db_session):
    client.post("/authors/", json={"first_name": "Another", "last_name": "Author"})
    response = client.get(f"/authors/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_update_author(db_session):
    client.post("/authors/", json={"first_name": "Anton", "last_name": "Pavlov", "birth_date": "2024-12-11"})

    response = client.put(f"/authors/1",
                          json={"first_name": "Updated", "last_name": "Author", "birth_date": "2024-09-10"})
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"


def test_create_book(db_session):
    response = client.post("/books/", json={"title": "Test Book", "description": "A test book.", "author_id": 1,
                                            "available_copies": 5})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"


def test_get_books(db_session):
    client.post("/books/", json={"title": "Test Book", "description": "A test book.", "author_id": 1,
                                 "available_copies": 5, "id": 1})
    response = client.get("/books/", params={"skip": 0, "limit": 10})
    print(response)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_borrow(db_session):
    response = client.post("/borrows/", json={"book_id": 1, "reader_name": "Test Reader", "borrow_date": "2023-01-01"})
    assert response.status_code == 200
    assert response.json()["reader_name"] == "Test Reader"


def test_return_borrow(db_session):
    client.post("/borrows/",
                json={"book_id": 1, "reader_name": "Test Reader", "borrow_date": "2023-01-01", "return_date": "null"})
    response = client.patch("/borrows/1/return", params={"return_date": "2023-01-10"})
    assert response.status_code == 200
    assert response.json()["return_date"] is not None


def test_delete_author(db_session):
    client.post("/authors/", json={"first_name": "Delete", "last_name": "Author"})

    response = client.delete(f"/authors/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
