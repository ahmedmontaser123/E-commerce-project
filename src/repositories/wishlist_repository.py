from modules.db.e_commerce.schemas import Wishlist
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class WishlistRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_to_wishlist(self, item: Wishlist):
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def get_wishlist(self, user_id: int):
        query = select(Wishlist).where(Wishlist.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_wishlist_item(self, user_id: int, product_id: int):
        query = select(Wishlist).where(
            Wishlist.user_id == user_id,
            Wishlist.product_id == product_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def remove_from_wishlist(self, user_id: int, product_id: int):
        stmt = delete(Wishlist).where(
            Wishlist.user_id == user_id,
            Wishlist.product_id == product_id
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return True
