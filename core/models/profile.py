from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from . import Base
from .model_mixins import UserRelationMixin


class Profile(UserRelationMixin, Base):
    _user_id_uniq: bool = True
    _user_back_populates: str | None = "profile"

    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
