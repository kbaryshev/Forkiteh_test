"""Содержит схемы валидации pydantic для кошельков."""

from pydantic import BaseModel, field_validator
from tronpy.keys import is_address


class Wallet(BaseModel):
	"""Схема для кошелька."""

	address: str
	balance: float
	bandwidth_free: int
	bandwidth_by_staking: int
	energy: int


class AddWalletsRequest(BaseModel):
	"""Схема для запроса добавление кошельков."""

	wallets_address: list[str]

	@field_validator('wallets_address')
	def validate_wallets_address(cls, value):
		for address in value:
			if not is_address(address):
				raise ValueError(f'Bad Tron address: {address}')

		return value
