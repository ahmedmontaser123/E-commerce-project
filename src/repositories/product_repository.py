from modules.db.e_commerce.schemas import User,Cart,Product,CartProduct,OrderProduct
from schemas import *
from sqlalchemy import select ,update
from sqlalchemy.ext.asyncio import AsyncSession


class ProductRepository:

    def __init__(self, session:AsyncSession = None):
        self.session = session 
    

    async def create_product(self, product:Product):
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product
    

    async def get_product_by_id(self, product_id:int):
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    

    async def get_all_products(self, skip: int, limit: int):
            query = (select(Product).offset(skip).limit(limit))
            result = await self.session.execute(query)
            return result.scalars().all()

    async def update_product(self,product:Product,request:ProductUpdateRequest):
        product.name = request.name
        product.price = request.price
        product.description = request.description
        product.stock = request.stock

        await self.session.commit()
        await self.session.refresh(product)

        return product
    


    async def delete_product(self, product_id:int):
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        product = result.scalar_one_or_none()

        if product is None:
            return False
        
        await self.session.delete(product)
        await self.session.commit()
        return True


    async def get_products_by_ids(self, product_ids: list[int]):
        query = select(Product).where(Product.id.in_(product_ids))
        result = await self.session.execute(query)
        return result.scalars().all()


    async def decrease_stock_by_cart(self, cart_id: int):
            stmt = (
                update(Product)
                 .values(
                        stock=Product.stock - (
                        select(CartProduct.quantity)
                              .where(
                                  CartProduct.product_id == Product.id,
                                  CartProduct.cart_id == cart_id
                                     )
                                    .scalar_subquery()
                                     )
                         )
        .where(
            Product.id.in_(
                select(CartProduct.product_id).where(
                    CartProduct.cart_id == cart_id
                )
            )
        )
    )

            await self.session.execute(stmt)

    async def increase_stock_by_order(self, order_id: int):
            stmt = (
                    update(Product).values(
                            stock=Product.stock + (select(OrderProduct.quantity).where(
                                                OrderProduct.product_id == Product.id,
                                               OrderProduct.order_id == order_id
                                                   ).scalar_subquery()
                                                    )
                                            )
                                            .where( Product.id.in_(select(OrderProduct.product_id).where(OrderProduct.order_id == order_id) ))
                    )

            await self.session.execute(stmt)