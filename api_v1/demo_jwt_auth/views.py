import secrets
import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/demo-auth", tags=["Demo auth"])


# --------------- BASIC AUTH -----------------
security = HTTPBasic()


demo_tokens_db = {
    "admin": "admin",
    "john": "pass1",
}


def get_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str | None:

    unauther_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )

    correct_pass = demo_tokens_db.get(credentials.username)
    if not correct_pass:
        raise unauther_exc

    elif not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_pass.encode("utf-8"),
    ):
        raise unauther_exc

    return credentials.username


@router.get("/basic_auth_with_check/")
async def demo_basic_auth_with_check(
    username: str = Depends(get_username),
) -> dict:

    return {
        "message": f"Hi, {username}",
        "username": username,
    }


# --------------- TOKEN AUTH (by header) -----------------
demo_tokens_db = {
    "c88e12e85664a07657961b939e1c1be1": "admin",
    "9a11e6fb7cd64b3e5a27f362bc7af36f": "john",
}


def get_username_by_static_auth_token(
    token: str = Header(alias="x-auth-token"),
) -> str | None:

    if username := demo_tokens_db.get(token):
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid token",
    )


@router.get("/some_header_auth/")
async def demo_some_header_auth(
    username: str = Depends(get_username_by_static_auth_token),
):
    return {
        "message": f"Hi, {username}",
        "username": username,
    }


# --------------- COOKIE AUTH -----------------
COOKIE_STORE: dict[str, dict] = {}
COOKIE_NAME = "MS_session_id"


async def session_gen() -> str:
    return uuid.uuid4().hex


async def get_session_data(
    session_id: str = Cookie(alias=COOKIE_NAME),
) -> dict:
    if session_data := COOKIE_STORE.get(session_id):
        return session_data
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="cookie not found",
    )


@router.post("/login-cookie/")
async def demo_auth_set_cookie(
    response: Response,
    username: str = Depends(get_username_by_static_auth_token),
):
    session_id = await session_gen()
    COOKIE_STORE[session_id] = {
        "username": username,
        "login_at": datetime.now(),
    }
    response.set_cookie(COOKIE_NAME, session_id)
    return {"result": "cookie is set"}


@router.get("/check-cookie/")
async def demo_auth_check_cookie(
    session_data: dict = Depends(get_session_data),
):
    return session_data


@router.get("/logout-cookie/")
async def demo_auth_logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_NAME),
    session_data: dict = Depends(get_session_data),
):
    COOKIE_STORE.pop(session_id)
    response.delete_cookie(COOKIE_NAME)
    username = session_data["username"]

    return {"message": f"Bye, {username}"}
