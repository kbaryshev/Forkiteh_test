"""Содержит тесты для работы с БД."""

from src.wallets.models import WalletModel
from src.wallets.service import add_wallets_to_db, get_wallets_from_db

from .conftest import TEST_ADDRESSES


async def test_add_to_db(get_session):
	"""Проверяет возможность добавить кошельки в БД."""
	wallet_models_1 = [
		WalletModel(address=address, balance=0, bandwidth_free=0, bandwidth_by_staking=0, energy=0)
		for address in TEST_ADDRESSES
	]
	await add_wallets_to_db(get_session, wallet_models_1)

	wallet_models_2 = await get_wallets_from_db(get_session)
	for wallet1, wallet2 in zip(wallet_models_1, wallet_models_2, strict=False):
		assert wallet1.address == wallet2.address
		assert wallet1.balance == wallet2.balance
		assert wallet1.bandwidth_free == wallet2.bandwidth_free
		assert wallet1.bandwidth_by_staking == wallet2.bandwidth_by_staking
		assert wallet1.energy == wallet2.energy
