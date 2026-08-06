from modules.db.e_commerce.schemas import ShippingAddress
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import ShippingRequest


class ShippingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_address(self, address: ShippingAddress):
        self.session.add(address)
        await self.session.commit()
        await self.session.refresh(address)
        return address

    async def get_address_by_id(self, address_id: int):
        query = select(ShippingAddress).where(ShippingAddress.id == address_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_address(self, address: ShippingAddress, data: ShippingRequest):
        address.addressline1 = data.addressline1
        address.addressline2 = data.addressline2
        address.city = data.city
        address.postalcode = data.postalcode
        address.country = data.country
        await self.session.commit()
        await self.session.refresh(address)
        return address
