from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.db.database import get_db_session
from schemas import PaymentRequest, PaymentResponse
from services.payment_service import PaymentService

payment_router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@payment_router.post("/{user_id}", response_model=PaymentResponse, status_code=201)
async def create_payment(
    user_id: int,
    request: PaymentRequest,
    session: AsyncSession = Depends(get_db_session)
):
    service = PaymentService(session)
    return await service.create_payment(user_id, request)


@payment_router.get("/{order_id}", response_model=PaymentResponse)
async def get_payment(
    order_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = PaymentService(session)
    return await service.get_payment(order_id)
