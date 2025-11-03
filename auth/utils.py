import uuid
from datetime import datetime, timedelta, UTC

import bcrypt
import jwt

from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire: int = settings.auth_jwt.access_token_exp,
):
    to_encode = payload.copy()

    now = datetime.now(UTC)
    expire = now + timedelta(seconds=expire)
    to_encode.update(
        {
            "exp": expire,
            "iat": now,
            "jti": str(uuid.uuid4()),
        }
    )

    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    encoded: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        jwt=encoded,
        key=public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(password: str) -> bytes:
    """Encrypt password with salt by bcrypt."""
    pwd_bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt=bcrypt.gensalt())


def validate_password(password: str, hashed_password: bytes) -> bool:
    """Compare received encrypted password with user encrypted password in DB."""
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
