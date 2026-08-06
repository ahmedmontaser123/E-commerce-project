from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from modules.db.e_commerce.schemas import ShippingAddress
from repositories import (
    UserRepository,
    ShippingRepository
)
from schemas import ShippingRequest


class ShippingService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)
        self.shipping_repo = ShippingRepository(session)

    async def create_address(self, user_id: int, request: ShippingRequest):
        user = await self.user_repo.get_user_by_id(user_id)
        if not user or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        address = ShippingAddress(
            userid=user_id,
            orderid=request.orderid,
            addressline1=request.addressline1,
            addressline2=request.addressline2,
            city=request.city,
            postalcode=request.postalcode,
            country=request.country,
        )

        return await self.shipping_repo.create_address(address)

    async def get_address(self, address_id: int):
        address = await self.shipping_repo.get_address_by_id(address_id)
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )

        return address

    async def update_address(self, user_id: int, address_id: int, request: ShippingRequest):
        user = await self.user_repo.get_user_by_id(user_id)
        if not user or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        address = await self.shipping_repo.get_address_by_id(address_id)
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )

        if address.userid != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to update this address"
            )

        return await self.shipping_repo.update_address(address, request)
