from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from . import Base


class Post(Base):
    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(Text, default="", server_default="")
    # Using 'int' in typehints we set constraint "nullable=False"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
