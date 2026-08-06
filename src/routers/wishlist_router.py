from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.db.database import get_db_session
from schemas import WishlistRequest, WishlistResponse
from services.wishlist_service import WishlistService

wishlist_router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist"]
)


@wishlist_router.post("/{user_id}", response_model=WishlistResponse, status_code=201)
async def add_to_wishlist(
    user_id: int,
    request: WishlistRequest,
    session: AsyncSession = Depends(get_db_session)
):
    service = WishlistService(session)
    return await service.add_to_wishlist(user_id, request)


@wishlist_router.get("/{user_id}",response_model=list[WishlistResponse])
async def get_wishlist(
    user_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = WishlistService(session)
    return await service.get_wishlist(user_id)


@wishlist_router.delete("/{user_id}/{product_id}",response_model=dict)
async def remove_from_wishlist(
    user_id: int,
    product_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = WishlistService(session)
    return await service.remove_from_wishlist(user_id, product_id)
