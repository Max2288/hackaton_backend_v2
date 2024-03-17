import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Класс, содержащий настройки приложения.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): URI для подключения к базе данных.
    """

    SQLALCHEMY_DATABASE_URI: str = 'postgresql+asyncpg://{0}:{1}@{2}/{3}'.format(
        os.environ["PG_USER"], os.environ["PG_PASSWORD"], os.environ["PG_HOST"], os.environ["DB_NAME"]
    )
    SCHEMA_NAME: str = os.environ["SCHEMA_NAME"]

    DESCRIPTION = "Stenagrafist"
    DEBUG: bool = False
    SERVICE_NAME = "Stenagrafist"
    API_V1_STR: str = "/api/v1"
    PORT: int = 5000

    SALT: str = "Max2288"
    ALGORITHM: str = "HS256"

    REDIS_HOST: str = os.environ["REDIS_HOST"]
    REDIS_PORT: int = os.environ["REDIS_PORT"]
    REDIS_PASSWORD: str = os.environ["REDIS_PASSWORD"]
    REDIS_CACHE_PREFIX: str = "Stenagrafist"
    REDIS_EXPIRE_TIME: int = 60

    KAFKA_BOOTSTRAP_SERVERS = ["kafka:29092"]
    KAFKA_TOPIC = "test_stena"
    KAFKA_CONSUMER_GROUP = "kafka_consumer_group"

    BUCKET_NAME = 'stena'

    SEARCH_ENGINE_HOST=os.environ["SEARCH_ENGINE_HOST"]