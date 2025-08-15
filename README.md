# Тестовое задание: Микросервис для Tron Wallet

[![Python 3.13+](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)
[![Pytest](https://img.shields.io/badge/Pytest-8.4.1-blue.svg)](https://pytest.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## О проекте

Проект представляет собой реализацию микросервиса на FastAPI для получения информации об адресах в сети TRON.

<details>
<summary><b>Техническое задание</b></summary>

-   Написать микросервис, который будет выводить информацию по адресу в сети трон, его bandwidth, energy, и баланс trx. Эндпоинт должен принимать в качестве входных данных адрес.
-   Каждый успешный запрос записывать в базу данных с указанием запрошенного кошелька.
-   Реализовать два эндпоинта:
    -   `POST` для получения информации о кошельке.
    -   `GET` для получения списка последних записей из БД с пагинацией.
-   Написать юнит/интеграционные тесты.

**Требования к стеку:** FastAPI, аннотации типов (typing), SQLAlchemy ORM, Tronpy, Pytest.
</details>

## Стек технологий

-   **Backend:** Python 3.13, FastAPI
-   **База данных:** PostgreSQL
-   **ORM и миграции:** SQLAlchemy, Alembic
-   **Взаимодействие с Tron:** TronPy
-   **Инструменты:** Uvicorn, UV (менеджер пакетов), Docker
-   **Тестирование и качество кода:** Pytest, Ruff

## Быстрый старт

### Предварительные требования

Перед началом работы убедитесь, что у вас установлены:
-   [Git](https://git-scm.com/)
-   [Python 3.13+](https://www.python.org/)
-   [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/)
-   [uv](https://github.com/astral-sh/uv) (рекомендуемый менеджер пакетов)

### Установка

1.  **Клонируйте репозиторий:**
    ```shell
    git clone https://github.com/kbaryshev/Forkiteh_test.git
    cd Forkiteh_test
    ```

2.  **Установите `uv` (если еще не установлен):**
    ```shell
    # Linux / macOS
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

3.  **Создайте виртуальное окружение:**
    ```shell
    uv venv
    ```

4.  **Установите зависимости проекта:**
    ```shell
    uv pip install .
    ```

5.  **Настройте переменные окружения:**
    Создайте файл `.env` в корне проекта, скопировав `.env.example`, и заполните его необходимыми данными (например, для подключения к БД).
    ```shell
    cp .env.example .env
    ```

## Запуск приложения

1.  **Запустите PostgreSQL в Docker-контейнере:**
    ```shell
    docker-compose up -d db
    ```

2. **Запустите сервер FastAPI:**
    ```shell
    uv run uvicorn src.main:app --reload
    ```

После запуска сервер будет доступен по адресу `http://127.0.0.1:8000`.
Интерактивная документация API (Swagger UI) находится по адресу [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API Эндпоинты

### 1. Получение информации о кошельке

-   **Endpoint:** `POST /wallets/`
-   **Описание:** Принимает адреса кошельков в сети TRON и возвращает информацию о них. Каждый успешный запрос сохраняется в базу данных.
-   **Тело запроса:**
    ```json
    {
      "wallets_address": ["string"]
    }
    ```
-   **Пример ответа:**
    ```json
    [
      {
        "address": "string",
        "balance": 0,
        "bandwidth_free": 0,
        "bandwidth_by_staking": 0,
        "energy": 0
      }
    ]
    ```

### 2. Получение истории запросов

-   **Endpoint:** `GET /wallets/`
-   **Описание:** Возвращает список последних запрошенных адресов с пагинацией.
-   **Query параметры:**
    -   `page` (int, опционально, по умолчанию 0): Номер страницы.
    -   `size` (int, опционально, по умолчанию 0): Количество записей на странице.
-   **Пример ответа:**
    ```json
    [
      {
        "address": "string",
        "balance": 0,
        "bandwidth_free": 0,
        "bandwidth_by_staking": 0,
        "energy": 0
      }
    ]
    ```

## Тестирование и качество кода

-   **Запуск тестов:**
    ```shell
    uv run pytest tests/
    ```

-   **Проверка линтером (Ruff):**
    ```shell
    uv run ruff check --fix
    ```

-   **Форматирование кода (Ruff):**
    ```shell
    uv run ruff format
    ```

---
## ✍️ Автор

Этот проект был разработан в рамках тестового задания.

**Кирилл Барышев**

-   **GitHub:** [@kbaryshev](https://github.com/kbaryshev)
-   **Email:** `baryshevkirr@gmail.com`

## ⚖️ Лицензия

Этот проект распространяется под лицензией MIT. Подробности можно найти в файле [LICENSE](LICENSE).