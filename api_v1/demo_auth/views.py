import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/demo-auth", tags=["Demo auth"])


security = HTTPBasic()


valid_db = {
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

    correct_pass = valid_db.get(credentials.username)
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
):
    return {
        "message": f"Hi, {username}",
        "username": username,
    }
