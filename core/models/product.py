from sqlalchemy.orm import Mapped

from core.models.base import Base


class Product_db(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
