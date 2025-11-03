import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import (
    db_helper,
    User,
    Profile,
    Post,
    Order,
    Product,
    OrderProductAssociation,
)


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(sesssion: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await sesssion.execute(stmt)
    # user: User | None = result.scalar_one_or_none()
    user: User | None = await sesssion.scalar(stmt)
    print(f"Got username: {username}.")
    print(f"Found user: {user}")
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    posts_info: list[dict],
) -> list[Post]:
    posts = [Post(user_id=user_id, **post_i) for post_i in posts_info]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts_join(session: AsyncSession):
    # first way to get the object with relation's type many-to-many
    stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)

    for user in users.unique():  # type: User
        print("**" * 10)
        print(user)
        for post in user.posts:
            print(post)


async def get_users_with_posts(session: AsyncSession):
    # second way to get the object with relation's type many-to-many
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)

    for user in users:  # type: User
        print("**" * 25)
        print("user", user)
        for post in user.posts:
            print("-" * 3, post)


async def get_post_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:  # type: Post
        print("post", post)
        print("author", post.user)


async def get_users_with_posts_and_profiles(session: AsyncSession):
    # first way to get the object with relation's type many-to-many
    stmt = (
        select(User)
        .options(joinedload(User.profile), selectinload(User.posts))
        .order_by(User.id)
    )
    users = await session.scalars(stmt)

    for user in users.unique():  # type: User
        print("**" * 10)
        print("user", user)
        print("profile_name", user.profile and user.profile.first_name)
        for post in user.posts:
            print(post)


async def get_profiles_with_users_and_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)  # join for filter
        .options(
            # join for optimized load
            joinedload(Profile.user).selectinload(User.posts)
        )
        # .where(User.username == "sam")
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)

    for profile in profiles:  # type: Profile
        print("profile.first_name", profile.first_name)
        print("user", profile.user)
        print("posts", profile.user.posts)


async def main_relations(session: AsyncSession):
    await create_user(session=session, username="john")
    await create_user(session=session, username="sam")
    user_john = await get_user_by_username(sesssion=session, username="john")
    user_sam = await get_user_by_username(sesssion=session, username="sam")

    profile_john = await create_user_profile(
        session=session,
        user_id=user_john.id,
        first_name="aaa",
        last_name="aaab",
    )
    profile_sam = await create_user_profile(
        session=session,
        user_id=user_sam.id,
        first_name="sss",
        last_name="aaaam",
    )

    await show_users_with_profiles(session=session)
    posts_info_john = [
        {"title": "sql1"},
        {"title": "sql2"},
    ]
    await create_posts(
        session=session, user_id=user_john.id, posts_info=posts_info_john
    )
    posts_info_sam = [
        {"title": "fast_api_1"},
        {"title": "fast_api_2"},
        {"title": "fast_api_3"},
    ]
    await create_posts(session=session, user_id=user_sam.id, posts_info=posts_info_sam)

    await get_users_with_posts(session=session)

    await get_post_with_authors(session=session)

    await get_users_with_posts_and_profiles(session=session)

    await get_profiles_with_users_and_posts(session=session)


async def create_order(
    session: AsyncSession,
    promo_code: str | None = None,
):
    order = Order(promo_code=promo_code)
    session.add(order)
    await session.commit()

    return order


async def create_product(
    session: AsyncSession,
    name: str,
    description: str,
    price: int,
):
    product = Product(
        name=name,
        description=description,
        price=price,
    )
    session.add(product)
    await session.commit()

    return product


async def create_orders_and_products(session: AsyncSession):
    order_1 = await create_order(session)
    order_2 = await create_order(session, promo_code="30code")

    mouse = await create_product(
        session=session,
        name="mouse 1",
        description="office mouse",
        price=150,
    )

    keyboard = await create_product(
        session=session,
        name="gaming",
        description="The best gamingboard",
        price=250,
    )
    display = await create_product(
        session=session,
        name="display",
        description="office display",
        price=500,
    )

    order_1 = await session.scalar(
        select(Order)
        .where(Order.id == order_1.id)
        .options(
            selectinload(Order.products),
        ),
    )
    order_2 = await session.scalar(
        select(Order)
        .where(Order.id == order_2.id)
        .options(
            selectinload(Order.products),
        ),
    )

    # add new product
    order_1.products.append(mouse)
    order_1.products.append(keyboard)

    # assign new value
    order_2.products = [mouse, display]

    await session.commit()


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)

    return list(orders)


async def demo_get_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session=session)

    for order in orders:
        print(order.id, order.promo_code, order.create_at, sep=", ")
        print("products: ")
        for product in order.products:
            print("-", product.id, product.name, product.price)
        print()


async def get_orders_with_products_assoc(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).options(
                joinedload(OrderProductAssociation.product)
            ),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)

    return list(orders)


async def demo_get_orders_with_assoc(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session=session)

    for order in orders:
        print(order.id, order.promo_code, order.create_at, sep=", ")
        print("products: ")
        for order_product_details in order.products_details:
            order_info = "; ".join(
                map(
                    str,
                    [
                        order_product_details.product.id,
                        order_product_details.product.name,
                        order_product_details.product.price,
                        f"qty: {order_product_details.quantity}",
                    ],
                )
            )
            print("-", order_info)
        print()


async def create_gift_for_existing_orders(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session=session)
    gift_product = await create_product(
        session=session,
        name="25% discount on jewelry",
        description="gift for you",
        price=0,
    )
    for order in orders:
        order.products_details.append(
            OrderProductAssociation(
                product=gift_product,
                quantity=1,
                unit_price=0,
            )
        )

    await session.commit()


async def demo_m2m(session: AsyncSession):
    # await create_orders_and_products(session=session)
    # await demo_get_orders_with_products_through_secondary(session=session)
    # await create_gift_for_existing_orders(session=session)
    await demo_get_orders_with_assoc(session=session)


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session=session)
        await demo_m2m(session=session)


if __name__ == "__main__":
    asyncio.run(main())
