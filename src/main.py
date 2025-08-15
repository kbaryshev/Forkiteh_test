"""Точка входа для всего приложения."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from alembic import command
from src.wallets.router import wallets_router

from .config import alembic_config


@asynccontextmanager
async def lifespan(app: FastAPI):
	"""Создает таблицы в БД при старте приложения и удаляет их после его выключения."""
	command.upgrade(alembic_config, 'head')
	yield


app = FastAPI(lifespan=lifespan)


app.include_router(wallets_router)
