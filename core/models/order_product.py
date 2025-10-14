from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from . import Order, Product


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "product_id",
            name="idx_uniq_order_product",
        ),
    )

    # If we create table without id we'll have to add composite primary key.
    # That means we must add primary_key=True for order_id and product_id
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    # association between Association -> Order
    order: Mapped["Order"] = relationship(back_populates="products_details")
    # association between Association -> Product
    product: Mapped["Product"] = relationship(back_populates="order_details")

    # extra fields
    # quantity of the products in the order
    quantity: Mapped[int] = mapped_column(default=1, server_default="1")
    # price at the time of the order
    unit_price: Mapped[int] = mapped_column(default=0, server_default="0")
