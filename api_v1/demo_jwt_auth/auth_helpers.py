from typing import Callable

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from api_v1.demo_jwt_auth.crud import users_db
from api_v1.users.schemas import UserSchema
from auth import utils as auth_utils
from core.config import settings

TOKEN_TYPE_FIELD = "token_type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/demo_jwt/login/")


# CREATE
def create_jwt(token_type: str, token_data: dict, expire_sec: int | None = None) -> str:
    payload = {TOKEN_TYPE_FIELD: token_type}
    payload.update(token_data)
    return auth_utils.encode_jwt(payload=payload, expire=expire_sec)


def create_access_token(user: UserSchema) -> str:
    """Release new jwt access token to authenticated user."""

    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }

    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_sec=settings.auth_jwt.access_token_exp,
    )


def create_refresh_token(user: UserSchema) -> str:
    """Release new jwt refresh token to authenticated user."""

    jwt_payload = {
        "sub": user.username,
    }

    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_sec=settings.auth_jwt.refresh_token_exp,
    )


# READ
def get_current_token_payload(
    token: str = Depends(oauth2_schema),
) -> dict:
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="token invalid",
        )
    return payload


def get_auth_user_by_token(
    expected_token_type: str, active_check: bool = True
) -> Callable:

    def inner(
        payload: dict = Depends(get_current_token_payload),
    ) -> UserSchema:
        token_type: str = payload.get(TOKEN_TYPE_FIELD)
        if token_type != expected_token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid token type {token_type!r} expected {ACCESS_TOKEN_TYPE!r}",
            )

        username: str = payload.get("sub") or payload.get("username")
        if not (user := users_db.get(username)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token invalid",
            )

        if active_check:
            if not user.active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="user inactive",
                )

        return user

    return inner


get_active_user_by_access_token = get_auth_user_by_token(ACCESS_TOKEN_TYPE)
get_active_user_by_refresh_token = get_auth_user_by_token(REFRESH_TOKEN_TYPE)
