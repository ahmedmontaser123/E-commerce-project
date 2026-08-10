from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete
from sqlalchemy.orm import joinedload
from modules.db.e_commerce.schemas import CartProduct


class CartProductRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, cart_product: CartProduct):
        self.session.add(cart_product)
        await self.session.commit()
        await self.session.refresh(cart_product)
        return cart_product

    async def get_by_cart_and_product(
        self,
        cart_id: int,
        product_id: int
    ):
        result = await self.session.execute(
            select(CartProduct).where(
                CartProduct.cart_id == cart_id,
                CartProduct.product_id == product_id
            )
        )
        return result.scalar_one_or_none()

    async def update(self, cart_product: CartProduct):
        await self.session.commit()
        await self.session.refresh(cart_product)
        return cart_product

    async def delete(self, cart_product: CartProduct):
        await self.session.delete(cart_product)
        await self.session.commit()
        await self.session.refresh(cart_product)
        return True

    async def delete_items(self, cart_id):
        stmt = delete(CartProduct).where(
                     CartProduct.cart_id == cart_id
                      )

        await self.session.execute(stmt)



    async def get_cart_items(self, cart_id: int):
        result = await self.session.execute(
        select(CartProduct)
        .options(joinedload(CartProduct.product))
        .where(CartProduct.cart_id == cart_id)
        )

        items = result.scalars().all()

        return items

   