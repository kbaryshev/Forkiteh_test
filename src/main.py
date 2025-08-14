"""Точка входа для всего приложения."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.wallets.router import wallets_router

from .database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
	"""Создает таблицы в БД при старте приложения и удаляет их после его выключения."""
	await create_tables()
	yield
	await delete_tables()


app = FastAPI(lifespan=lifespan)


app.include_router(wallets_router)
