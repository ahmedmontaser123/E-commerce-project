from modules.db.e_commerce.schemas import Review
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ReviewRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_review(self, review: Review):
        self.session.add(review)
        await self.session.commit()
        await self.session.refresh(review)
        return review

    async def get_reviews_by_product(self, product_id: int):
        query = select(Review).where(Review.product_id == product_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_review_by_id(self, review_id: int):
        query = select(Review).where(Review.id == review_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_review(self, user_id: int, product_id: int):
        query = select(Review).where(
            Review.user_id == user_id,
            Review.product_id == product_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete_review(self, review: Review):
        await self.session.delete(review)
        await self.session.commit()
        return True
