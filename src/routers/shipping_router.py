from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.db.database import get_db_session
from schemas import ShippingRequest, ShippingResponse
from services.shipping_service import ShippingService

shipping_router = APIRouter(
    prefix="/shipping",
    tags=["Shipping"]
)


@shipping_router.post("/{user_id}", response_model=ShippingResponse, status_code=201)
async def create_address(
    user_id: int,
    request: ShippingRequest,
    session: AsyncSession = Depends(get_db_session)
):
    service = ShippingService(session)
    return await service.create_address(user_id, request)


@shipping_router.put("/{user_id}/{address_id}", response_model=ShippingResponse)
async def update_address(
    user_id: int,
    address_id: int,
    request: ShippingRequest,
    session: AsyncSession = Depends(get_db_session)
):
    service = ShippingService(session)
    return await service.update_address(user_id, address_id, request)


@shipping_router.get("/{address_id}", response_model=ShippingResponse)
async def get_address(
    address_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = ShippingService(session)
    return await service.get_address(address_id)
