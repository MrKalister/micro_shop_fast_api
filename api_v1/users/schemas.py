from pydantic import BaseModel, EmailStr, Field, ConfigDict


class BaseUser(BaseModel):
    username: str = Field(min_length=3, max_length=25)
    email: EmailStr


class UserCreate(BaseUser):
    pass


class User(BaseUser):
    id: int


class UserSchema(BaseModel):
    # to get strict types for class variables
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
