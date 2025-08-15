## О проекте

Проект содержит реализацию тестового задания по указанному ниже ТЗ.

<details>

<summary>ТЗ</summary>

Написать микросервис, который будет выводить информацию по адресу в сети трон,
его bandwidth, energy, и баланс trx, ендпоинт должен принимать входные данные - адрес.
Каждый запрос писать в базу данных, с полями о том какой кошелек запрашивался.
Написать юнит/интеграционные тесты.

У сервиса 2 ендпоинта
- POST
- GET для получения списка последних записей из БД, включая пагинацию

2 теста
- интеграционный на ендпоинт
- юнит на запись в бд

Примечания: использовать FastAPI, аннотацию(typing), SQLAlchemy ORM,
для удобства взаимодействия с троном можно использовать tronpy, для тестов - Pytest.

</details>

В проекте иcпользованы следующие технологии:
- Python 3.13
- FastAPI
- SQLAlchemy(asyncpg и psycopg2)
- Alembic
- PostgreSQL
- Pytest
- TronPy
- Uvicorn

## Установка зависимостей

Установка uv
```shell
wget -qO- https://astral.sh/uv/install.sh | sh
```

Клонирование репозитория
```shell
git clone https://github.com/kbaryshev/Forkiteh_test.git
```

Переход в директорию проекта
```shell
cd Forkiteh_test
```

Создание venv
```shell
uv venv
```

Установка всех python зависимостей для проекта
```shell
uv pip install .
```

## Запуск

Запуск PostgreSQL в контейнере
```shell
docker-compose up -d db
```

Запуск сервера
```shell
uv run uvicorn src.main:app --reload
```

Запуск тестов
```shell
uv run pytest tests/
```

Линтер
```shell
uv run ruff check --fix
```

Форматтер
```shell
uv run ruff format 
```

