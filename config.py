import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_DB: str

    PFP_PATH: str = os.getcwd() + "/data/pfp/"

    DEBUG_ENGINE: bool = False


settings = Settings()
