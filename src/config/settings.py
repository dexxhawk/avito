from os import environ

from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    ENV: str = environ.get("ENV", "local")
    PATH_PREFIX: str = environ.get("PATH_PREFIX", "/api")
    APP_HOST: str = environ.get("APP_HOST", "http://127.0.0.1")
    APP_PORT: int = int(environ.get("APP_PORT", 8080))
    SERVER_ADDRESS: str = environ.get("SERVER_ADDRESS", "")

    POSTGRES_DB: str = environ.get("POSTGRES_DATABASE", "tender")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = environ.get("POSTGRES_USERNAME", "postgres")
    POSTGRES_PORT: int = int(environ.get("POSTGRES_PORT", "5432")[-4:])
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "postgres")
    POSTGRES_CONN: str = environ.get("POSTGRES_CONN", "")
    DB_CONNECT_RETRY: int = environ.get("DB_CONNECT_RETRY", 20)
    DB_POOL_SIZE: int = environ.get("DB_POOL_SIZE", 15)

    # @property
    # def database_settings(self) -> dict:
    #     return {
    #         "database": self.POSTGRES_DB,
    #         "user": self.POSTGRES_USER,
    #         "password": self.POSTGRES_PASSWORD,
    #         "host": self.POSTGRES_HOST,
    #         "port": self.POSTGRES_PORT,
    #     }

    @property
    def database_uri(self) -> str:
        return self.POSTGRES_CONN


def get_settings() -> DefaultSettings:
    env = environ.get("ENV", "local")
    return DefaultSettings()
