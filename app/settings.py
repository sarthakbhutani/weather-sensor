from os import getenv

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
ENV = getenv("ENV")

# ENV -----------------
LOG_LEVEL = getenv("LOG_LEVEL")
SERVICE_NAME = getenv("SERVICE_NAME")
BASE_ROUTE = getenv("BASE_ROUTE")
DB_USERNAME = getenv("DB_USERNAME")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_NAME = getenv("DB_NAME")
DB_HOST = getenv("DB_HOST")
DB_PORT = int(getenv("DB_PORT","5432"))