"""Содержит настройки и фикстуры для тестов."""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from alembic import command
from src.config import alembic_config
from src.database import DB_URL, Base, get_db_session
from src.main import app

TEST_ADDRESSES = [
	'TGMWZxGvUecFCF9vHeaqRe2F6wja7nZmT1',
	'TF78UY3zxoTo6yP6Hyx125CCrJ4Eoevz1C',
	'TFhn1Sz1HFzBt2UmVETLQsBCAKNiHqmLCK',
	'TVzcKsQDghQKnw3kxqz4NKd6A4D9BnQGEV',
	'TENn6wzfdWcY4ToboSfxjdx4qnFXVcug3o',
	'TUz4nTU75z5oK4pYaVipkSDQ3Bi2DXdQT8',
	'TJP84f91HwWPCTGtdV8h5wzLpuQezZeU79',
	'TEh7ZvSEa65PMttmNqhNzqYmjqotK7e9vQ',
]

BAD_ADDRESSES = ['TGqweqwegsgagfwAGSAFGA123FSFWSFSDG']


@pytest.fixture
async def get_engine():
	"""Возвращает движок для БД."""
	db_engine = create_async_engine(DB_URL)
	yield db_engine
	await db_engine.dispose()


@pytest.fixture
async def get_session_maker(get_engine):
	"""Возвращает sessiomaker."""
	session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=get_engine, class_=AsyncSession)
	yield session_maker


@pytest.fixture(scope='function')
async def get_session(get_session_maker):
	"""Возвращает сессию БД."""
	async with get_session_maker() as session:
		yield session
		await session.rollback()


@pytest.fixture(scope='session')
async def http_client():
	"""Http клиент для запросов в тестах."""
	async with AsyncClient(transport=ASGITransport(app=app), base_url='http://127.0.0.1:8000') as client:
		yield client


@pytest.fixture(scope='function', autouse=True)
async def override_db(get_session):
	"""Фикстура для замены БД в приложении на тестовую."""
	async def override_get_db():
		yield get_session

	app.dependency_overrides[get_db_session] = override_get_db


@pytest.fixture(scope='function', autouse=True)
async def create_tables():
	"""Фикстура для создания и удаления таблиц в БД."""
	command.upgrade(alembic_config, 'head')
	yield
	command.downgrade(alembic_config, 'base')
