import os

from dotenv import load_dotenv

from src.config.definitions import ENV_PATH

load_dotenv(ENV_PATH)

DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_URL = (
    os.getenv("DB_URL")
    or f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
)

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
