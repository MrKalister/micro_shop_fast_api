from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR: Path = Path(__file__).parent.parent
DB_PATH: Path = BASE_DIR / "sqlite_db"


class DBSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = True  # TODO: debug only


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_exp: int = 60 * 10  # 10 minutes
    refresh_token_exp: int = 60 * 60 * 24 * 30  # 30 days


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DBSettings = DBSettings()

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
