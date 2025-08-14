"""Содержит роутер для работы с кошельками."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_session

from .schemas import AddWalletsRequest, Wallet
from .service import add_wallets_to_db, get_wallets_data, get_wallets_from_db

wallets_router = APIRouter(prefix='/wallets', tags=['wallets'])


@wallets_router.get('/', response_model=list[Wallet])
async def get_wallets(
	session: AsyncSession = Depends(get_db_session),
	page: int = Query(ge=0, default=None),
	page_size: int = Query(ge=0, default=None),
):
	"""Возвращает все кошельки попадающие под условия пагинации."""
	wallets = await get_wallets_from_db(session=session, page=page, page_size=page_size)
	return wallets


@wallets_router.post('/', response_model=list[Wallet])
async def add_wallets(
	wallets_request_data: AddWalletsRequest,
	session: AsyncSession = Depends(get_db_session),
):
	"""Возвращает данные кошельков и добавляет их в БД."""
	wallets = await get_wallets_data(wallets_request_data.wallets_address)
	await add_wallets_to_db(session=session, wallets=wallets)
	return wallets
