from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer

from api_v1.demo_jwt_auth.auth_helpers import (
    create_access_token,
    create_refresh_token,
    get_current_token_payload,
    get_active_user_by_refresh_token,
    get_active_user_by_access_token,
)
from api_v1.demo_jwt_auth.crud import users_db
from api_v1.users.schemas import UserSchema, TokenInfo
from auth import utils as auth_utils

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix="/demo_jwt",
    tags=["Demo JWT"],
    dependencies=[Depends(http_bearer)],
)


# Login Helper
def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid login or password",
    )
    if not (user := users_db.get(username)):
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password, hashed_password=user.password
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


# Endpoints
@router.post("/login/", response_model=TokenInfo)
def auth_user_jwt(user: UserSchema = Depends(validate_auth_user)):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
def refresh_auth_jwt(
    user: UserSchema = Depends(get_active_user_by_refresh_token),
):
    access_token = create_access_token(user)
    return TokenInfo(access_token=access_token)


@router.get("/users/me/")
def get_user_info(
    payload: dict = Depends(get_current_token_payload),
    active_current_user: UserSchema = Depends(get_active_user_by_access_token),
) -> dict:
    return {
        "username": active_current_user.username,
        "email": active_current_user.email,
        "logged_in_at": payload.get("iat"),
    }
