from fastapi import APIRouter

from api_v1.users import crud
from api_v1.users.schemas import UserCreate

router = APIRouter(tags=["Users"])


@router.post("/")
def create_user(user: UserCreate):
    return crud.create_user(user_in=user)
