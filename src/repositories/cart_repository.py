from modules.db.e_commerce.schemas import Cart,CartProduct,Product
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import CartRequest


class CartRepository:

    def __init__(self,session: AsyncSession = None):
        self.session = session
    
    async def create_cart(self, cart_data:CartRequest):
        db_cart = Cart(
            user_id = cart_data.user_id
        )
        self.session.add(db_cart)
        await self.session.commit()
        await self.session.refresh(db_cart)
        return db_cart
    
    async def get_cart_by_userid(self, user_id:int):
        query = select(Cart).where(Cart.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete_cart(self, cart:Cart):
        await self.session.delete(cart)
        await self.session.commit()
        return True
    