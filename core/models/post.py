from sqlalchemy import String, Text
from sqlalchemy.orm import mapped_column, Mapped

from . import Base
from .model_mixins import UserRelationMixin


class Post(UserRelationMixin, Base):
    _user_back_populates: str | None = "posts"

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(Text, default="", server_default="")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r}, user_id={self.user_id})"

    __repr__ = __str__
