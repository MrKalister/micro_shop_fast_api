from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from . import OrderProductAssociation


class Order(Base):
    promo_code: Mapped[str | None]
    create_at: Mapped[datetime] = mapped_column(
        # it'll be uses for example,
        # if we create an obj directly in database.
        server_default=func.now(),
        default=datetime.now,
    )
    # many-to-many relationship to Product, bypassing the `Association` class
    # products: Mapped[List["Product"]] = relationship(
    #     secondary="order_product_association",
    #     back_populates="orders",
    # )

    # association between Order -> Association -> Product
    products_details: Mapped[List["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )
