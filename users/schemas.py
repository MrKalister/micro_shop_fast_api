from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    username: str = Field(min_length=3, max_length=25)
    email: EmailStr
