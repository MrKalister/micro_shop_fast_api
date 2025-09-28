import os
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent
DB_PATH: str = os.path.join(BASE_DIR, "sqlite_db")


class DBSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = True  # TODO: debug only


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DBSettings = DBSettings()


settings = Settings()
