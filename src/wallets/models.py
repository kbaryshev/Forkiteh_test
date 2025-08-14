"""Содержит модели базы данных для кошельков."""

from sqlalchemy import Column, Float, Integer, String

from src.database import Base


class WalletModel(Base):
	"""Модель БД для кошельков."""

	__tablename__ = 'wallets'

	id = Column(Integer, primary_key=True)
	address = Column(String, unique=True)
	balance = Column(Float, nullable=False)
	bandwidth_free = Column(Integer, nullable=False)
	bandwidth_by_staking = Column(Integer, nullable=False)
	energy = Column(Integer, nullable=False)
