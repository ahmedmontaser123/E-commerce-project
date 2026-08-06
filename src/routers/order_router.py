from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import *
from modules.db.database import get_db_session
from services.order_service import OrderService

order_router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@order_router.post("/{user_id}",response_model=OrderResponse)
async def create_order(
    user_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = OrderService(session)
    order = await service.create_order_id(user_id)
    return order


@order_router.get("/{order_id}",response_model =list[OrderProductResponse])
async def get_order(
    order_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = OrderService(session)
    return await service.get_order(order_id)


@order_router.put("/{order_id}/cancel",response_model=dict)
async def cancel_order(
    order_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = OrderService(session)
    return await service.cancel_order(order_id)