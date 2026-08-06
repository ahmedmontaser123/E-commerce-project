from modules.db.e_commerce.schemas import User,Cart,Product,Order,OrderProduct,CartProduct
from sqlalchemy import select ,insert
from sqlalchemy.ext.asyncio import AsyncSession


class OrderRepository:

    def __init__(self, session:AsyncSession):
        self.session = session


    async def create_order(self,order:Order):
        self.session.add(order)
        await self.session.flush()
        return order

    async def create_order_products(self, order_id: int, cart_id: int):
        stmt = insert(OrderProduct).from_select(
                ["order_id", "product_id", "quantity"],
                select(
                  order_id,
                  CartProduct.product_id,
                  CartProduct.quantity,
                  
                  )
                    .join(Product, Product.id == CartProduct.product_id)
                    .where(CartProduct.cart_id == cart_id)
                )

        await self.session.execute(stmt)

    async def get_order_product(self, order_id):
            stmt = select(OrderProduct).where(OrderProduct.order_id == order_id)
            result = await self.session.execute(stmt)
            return result.scalars().all()

    async def get_order_id(self, order_id):
                stmt = select(Order).where(Order.id == order_id)
                result = await self.session.execute(stmt)
                return result.scalar_one_or_none()

    async def delete_order(self, order:Order):
          await self.session.commit()
          await self.session.refresh(order)
          return True