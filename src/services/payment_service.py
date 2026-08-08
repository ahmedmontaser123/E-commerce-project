from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from modules.db.e_commerce.schemas import Payment, PaymentStatus
from repositories import (
    UserRepository,
    OrderRepository,
    PaymentRepository
)
from schemas import PaymentRequest


class PaymentService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)
        self.order_repo = OrderRepository(session)
        self.payment_repo = PaymentRepository(session)

    async def create_payment(self, user_id: int, request: PaymentRequest):
        user = await self.user_repo.get_user_by_id(user_id)
        if not user or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        order = await self.order_repo.get_order_id(request.order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        if order.userid != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Order does not belong to this user"
            )

        existing_payment = await self.payment_repo.get_payment_by_order(request.order_id)
        if existing_payment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment already exists for this order"
            )


        if request.amount < order.total:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment amount is less than the order total"
            )

        payment = Payment( 
            order_id=request.order_id,
            amount=request.amount,
            payment_method=request.payment_method,
            payment_status=PaymentStatus.COMPLETED,
            transaction_id=request.transaction_id,
        )

        return await self.payment_repo.create_payment(payment)

    async def get_payment(self, order_id: int):
        payment = await self.payment_repo.get_payment_by_order(order_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )

        return payment
