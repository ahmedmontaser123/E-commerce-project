from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from modules.db.e_commerce.schemas import Wishlist
from repositories import (
    UserRepository,
    ProductRepository,
    WishlistRepository
)
from schemas import WishlistRequest


class WishlistService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)
        self.product_repo = ProductRepository(session)
        self.wishlist_repo = WishlistRepository(session)

    async def add_to_wishlist(self, user_id: int, request: WishlistRequest):
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

        existing = await self.wishlist_repo.get_wishlist_item(user_id, request.product_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product already in wishlist"
            )

        item = Wishlist(
            user_id=user_id,
            product_id=request.product_id,
        )

        return await self.wishlist_repo.add_to_wishlist(item)

    async def get_wishlist(self, user_id: int):
        user = await self.user_repo.get_user_by_id(user_id)
        if not user or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return await self.wishlist_repo.get_wishlist(user_id)

    async def remove_from_wishlist(self, user_id: int, product_id: int):
        user = await self.user_repo.get_user_by_id(user_id)
        if not user or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        item = await self.wishlist_repo.get_wishlist_item(user_id, product_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found in wishlist"
            )

        await self.wishlist_repo.remove_from_wishlist(user_id, product_id)
        return {"message": "Product removed from wishlist"}
