from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from modules.db.database import get_db_session
from services import CartService
from schemas import (
    CartResponse,
    CartRequest,
    CartItemRequest,
    CartItemResponse,
    UpdateCartItemRequest,
)

cart_router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@cart_router.post("/{user_id}", response_model=dict)
async def create_cart(
    user_id: int,
    cart_data: CartRequest,
    session: AsyncSession = Depends(get_db_session)
):
    service = CartService(session)
    await service.create_cart(user_id, cart_data)
    return {"message":"cart add successfully"}


@cart_router.post("/{user_id}/items", response_model=dict)
async def add_item(
    user_id: int,
    item: CartItemRequest,
    session: AsyncSession = Depends(get_db_session)
):
    service = CartService(session)
    await service.add_items(user_id, item)
    return {"message":"add item sucessfully"}


@cart_router.get("/{user_id}/items", response_model=list[CartItemResponse])
async def get_items(
    user_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = CartService(session)
    return await service.get_items(user_id)


@cart_router.put("/{user_id}/items/{item_id}", response_model=dict)
async def update_quantity(
    user_id: int,
    item_id: int,
    data: UpdateCartItemRequest,
    session: AsyncSession = Depends(get_db_session)
):
    service = CartService(session)
    await service.update_quantity(user_id, item_id, data)
    return {"message":"updated successfully"}


@cart_router.delete("/{user_id}/items/{item_id}", response_model=dict)
async def delete_item(
    user_id: int,
    item_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = CartService(session)
    return await service.delete_item(user_id, item_id)


@cart_router.delete("/{user_id}", response_model=dict)
async def delete_cart(
    user_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = CartService(session)
    await service.delete_cart(user_id)
    return {"message":"the cart deleted successfully"}