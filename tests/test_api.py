"""Содержит тесты для api кошельков."""

import pytest

from .conftest import BAD_ADDRESSES, TEST_ADDRESSES


async def test_add_wallets(http_client):
	"""Проверяет корректный сценарий добавления кошельков."""
	response_add_wallets = await http_client.post(
		'/wallets/',
		json={'wallets_address': TEST_ADDRESSES},
	)
	assert response_add_wallets.status_code == 200

	response_get_wallets = await http_client.get('/wallets/')
	assert response_get_wallets.status_code == 200
	assert len(response_get_wallets.json()) == len(TEST_ADDRESSES)


async def test_add_wallets_negative_wallet_already_exist(http_client):
	"""
	Проверяет негативный сценарий при отправке адреса кошелька который уже есть в базе,
	а также отсутствие адресов из запроса с продублированным адресом.
	"""
	response_add_wallets_1 = await http_client.post(
		'/wallets/',
		json={'wallets_address': TEST_ADDRESSES[:5]},
	)
	assert response_add_wallets_1.status_code == 200

	response_add_wallets_2 = await http_client.post(
		'/wallets/',
		json={'wallets_address': TEST_ADDRESSES[:4]},
	)
	assert response_add_wallets_2.status_code == 409

	response_get_wallets = await http_client.get('/wallets/')
	assert response_get_wallets.status_code == 200

	assert response_get_wallets.json() == response_add_wallets_1.json()


async def test_add_wallets_negative_bad_address(http_client):
	"""Проверяет негативный сценарий при отправке некоректного адреса кошелька."""
	response_add_wallets = await http_client.post(
		'/wallets/',
		json={'wallets_address': BAD_ADDRESSES},
	)
	assert response_add_wallets.status_code == 422


@pytest.mark.parametrize(
	'params', [{}, {'page': 0, 'page_size': 2}, {'page': 1, 'page_size': 3}, {'page': 2, 'page_size': 3}]
)
async def test_get_wallets_pagination(http_client, params):
	"""Проверяет корректный сценарий получения кошельков с настройками пагинации."""
	response_add_wallets = await http_client.post(
		'/wallets/',
		json={'wallets_address': TEST_ADDRESSES},
	)
	assert response_add_wallets.status_code == 200

	response_get_wallets = await http_client.get('/wallets/', params=params)
	assert response_get_wallets.status_code == 200
	if params:
		page = params['page']
		page_size = params['page_size']
		assert (
			response_add_wallets.json()[page * page_size : page * page_size + page_size] == response_get_wallets.json()
		)
