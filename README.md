# Web-приложение для определения заполненных форм.

REST API с использованием FastAPI для управления библиотечным каталогом. 
API позволяет работать с книгами, авторами и выдачей книг читателям.

## Структура проекта
1. Папка core содержит в себе cruds, models, schemas - вся логику для создания моделей и взаимодействий с ними. 
2. test_api.py -  скрипты для тестирования реализован на pytest.
3. library.db - файл с тестовой базой данных (появится при запуске проекта).
4. database.py - скрипт для создания тестовой базы данных.
5. requirements.txt - файл содержащий  список всех необходимых библиотек и их версий, которые требуются для работы проекта.
6. main.py - основной файл приложения.
7. README.md - файл с инструкциями.


 
## Инструкции по настройке и запуску

1. Установка проекта:

```

git clone https://github.com/inzord/LibraryManagement.git

```

2. Установка необходимых зависимостей:

```

pip install -r requirements.txt

```

3. Запуск проекта:

```

uvicorn main:app --reload

```

4. Запуск тестов:

Переходим в папку с тестами cd tests.

```

python test_api.py

```
5. Документация:

Переходим по ссылке:

```

http://127.0.0.1:8000/docs

```