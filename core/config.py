import os
from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    file_path: str = os.path.join(BASE_DIR, "sqlite_db")
    db_url: str = f"sqlite+aiosqlite:///{file_path}"
    db_echo: bool = True  # TODO: debug only


settings = Settings()
