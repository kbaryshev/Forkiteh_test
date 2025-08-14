"""Содержит подключение к базе данных."""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from .config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER

DB_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(DB_URL, echo=False)

session_maker = async_sessionmaker(
	autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def create_tables():
	"""Создает все таблицы в БД."""
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
	"""Удаляет все таблицы из БД."""
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)


async def get_db_session():
	"""Возвращает сессию для работы с БД."""
	async with session_maker() as session:
		yield session
