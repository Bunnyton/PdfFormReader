import os
from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import Field, Extra
from typing import ClassVar


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()