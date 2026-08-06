from modules.db.e_commerce.schemas import Payment
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_payment(self, payment: Payment):
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def get_payment_by_order(self, order_id: int):
        query = select(Payment).where(Payment.order_id == order_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
