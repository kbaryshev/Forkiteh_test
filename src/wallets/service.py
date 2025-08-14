"""Содержит бизнес логику для работы с кошельками."""

import asyncio

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron

from src.config import TRON_NETWORK

from .exceptions import WalletAlreadyExistException
from .models import WalletModel
from .schemas import Wallet


async def get_wallet_data(account_address: str) -> Wallet:
	"""Возвращает данные по кошельку с адресом account_address из сети tron."""
	async with AsyncTron(network=TRON_NETWORK) as client:
		account_resource_info = await client.get_account_resource(account_address)
		account_balance = await client.get_account_balance(account_address)

	balance = float(account_balance)

	bandwidth_free = account_resource_info.get('freeNetLimit', 0) - account_resource_info.get('freeNetUsed', 0)
	bandwidth_by_staking = account_resource_info.get('NetLimit', 0) - account_resource_info.get('NetUsed', 0)

	energy = account_resource_info.get('EnergyLimit', 0) - account_resource_info.get('EnergyUsed', 0)

	return Wallet(
		address=account_address,
		balance=balance,
		bandwidth_free=bandwidth_free,
		bandwidth_by_staking=bandwidth_by_staking,
		energy=energy,
	)


async def get_wallets_data(addresses: list[str]) -> list[Wallet]:
	"""Возвращает данные по кошелькам с адресами из addresses из сети tron."""
	tasks = [get_wallet_data(addr) for addr in addresses]

	result = await asyncio.gather(*tasks)
	return result


async def add_wallets_to_db(session: AsyncSession, wallets: list[Wallet]):
	"""
	Добавляет все переданные о кошельках данные в БД.
	При совпадении адреса у кошелька в wallets и БД бросает исключение,
	откатывает все кошельки записанные в рамках этого запроса.
	"""
	wallet_models = [
		WalletModel(
			address=wallet.address,
			balance=wallet.balance,
			bandwidth_free=wallet.bandwidth_free,
			bandwidth_by_staking=wallet.bandwidth_by_staking,
			energy=wallet.energy,
		)
		for wallet in wallets
	]
	try:
		session.add_all(wallet_models)
		await session.commit()
	except IntegrityError as err:
		await session.rollback()
		raise WalletAlreadyExistException(wallet_address=err.params[0]) from err


async def get_wallets_from_db(
	session: AsyncSession, page: int | None = None, page_size: int | None = None
) -> list[Wallet]:
	"""Возвращает все кошельки из БД согласно условиям пагинации."""
	page_offset = None if (page is None or page_size is None) else page * page_size
	result = await session.execute(select(WalletModel).offset(page_offset).limit(page_size))
	return [
		Wallet(
			address=wallet_model.address,
			balance=wallet_model.balance,
			bandwidth_free=wallet_model.bandwidth_free,
			bandwidth_by_staking=wallet_model.bandwidth_by_staking,
			energy=wallet_model.energy,
		)
		for wallet_model in result.scalars().all()
	]
