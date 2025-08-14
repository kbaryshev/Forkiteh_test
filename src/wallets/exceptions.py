"""Содержит исключения возникающие при работе с кошельками."""

from fastapi import HTTPException, status


class WalletAlreadyExistException(HTTPException):
	"""Исключение для дублирования уникального адреса при попытке добавления кошелька."""

	def __init__(self, wallet_address):
		super().__init__(
			status_code=status.HTTP_409_CONFLICT, detail=f'Wallet with address: {wallet_address} already exist.'
		)
