from typing import List

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ProductCreate, ProductUpdate, ProductUpdatePartial
from core.models import Product_db


async def get_products(
    session: AsyncSession,
) -> list[Product_db]:
    stmt = select(Product_db).order_by(Product_db.id)
    result: Result = await session.execute(stmt)
    # scalars() extracts Product from each tuple
    # all() makes list from generator
    products = result.scalars().all()
    return list(products)


async def get_product(
    session: AsyncSession,
    product_id: int,
) -> Product_db | None:
    return await session.get(Product_db, product_id)


async def create_product(
    session: AsyncSession,
    product_in: ProductCreate,
) -> Product_db:
    product = Product_db(**product_in.model_dump())
    session.add(product)
    await session.commit()
    # await session.refresh(product)
    return product


async def update_product(
    session: AsyncSession,
    product: Product_db,
    product_update: ProductUpdate | ProductUpdatePartial,
    partial: bool = False,
) -> Product_db:
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    # await session.refresh(product)
    return product


async def delete_product(
    session: AsyncSession,
    product: Product_db,
):
    await session.delete(product)
    await session.commit()
