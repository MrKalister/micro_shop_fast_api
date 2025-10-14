from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from . import OrderProductAssociation


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    # many-to-many relationship to Order, bypassing the `Association` clas
    # orders: Mapped[List["Order"]] = relationship(
    #     secondary="order_product_association",
    #     back_populates="products",
    # )

    # association between Product -> Association -> Order
    order_details: Mapped[List["OrderProductAssociation"]] = relationship(
        back_populates="product"
    )
