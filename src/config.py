"""Содержит конфигурацию проекта."""

from pathlib import Path

from environs import Env

PROJECT_ROOT_DIR = Path.cwd()
ENV_FILE_PATH = PROJECT_ROOT_DIR.joinpath('.env')

env = Env()
env.read_env(ENV_FILE_PATH)

TRON_NETWORK = env('TRON_NETWORK', default='shasta')

POSTGRES_USER = env('POSTGRES_USER')
POSTGRES_PASSWORD = env('POSTGRES_PASSWORD')
POSTGRES_DB = env('POSTGRES_DB')
POSTGRES_HOST = env('POSTGRES_HOST')
POSTGRES_PORT = env('POSTGRES_PORT')
