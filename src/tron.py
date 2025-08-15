"""Содержит клиент для работы с tron."""

from tronpy import AsyncTron

from src.config import TRON_NETWORK


async def get_tron_client():
	"""Возвращает клиент tron."""
	async with AsyncTron(network=TRON_NETWORK) as tron_client:
		yield tron_client
