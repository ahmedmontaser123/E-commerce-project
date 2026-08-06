from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from modules.db.e_commerce.schemas import Review, UserRole
from repositories import (
    UserRepository,
    ProductRepository,
    ReviewRepository
)
from schemas import ReviewRequest


class ReviewService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)
        self.product_repo = ProductRepository(session)
        self.review_repo = ReviewRepository(session)

    async def create_review(self, user_id: int, request: ReviewRequest):
        user = await self.user_repo.get_user_by_id(user_id)
        if not user or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        product = await self.product_repo.get_product_by_id(request.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        existing = await self.review_repo.get_user_review(user_id, request.product_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already reviewed this product"
            )

        review = Review(
            user_id=user_id,
            product_id=request.product_id,
            rating=request.rating,
            comment=request.comment,
        )

        return await self.review_repo.create_review(review)

    async def get_reviews_by_product(self, product_id: int):
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        return await self.review_repo.get_reviews_by_product(product_id)

    async def delete_review(self, user_id: int, review_id: int):
        user = await self.user_repo.get_user_by_id(user_id)
        if not user or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        review = await self.review_repo.get_review_by_id(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )

        if review.user_id != user_id and user.role != UserRole.Admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to delete this review"
            )

        await self.review_repo.delete_review(review)
        return {"message": "Review deleted successfully"}
