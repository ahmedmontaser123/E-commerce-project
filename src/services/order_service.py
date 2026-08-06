from sqlalchemy.ext.asyncio import AsyncSession
from modules.db.e_commerce.schemas import User,UserRole,Order,OrderProduct,orderstatus
from schemas import UserCreateRequest,CartRequest,CartItemResponse,CartItemRequest,UpdateCartItemRequest
from fastapi import HTTPException, status
from modules.db.e_commerce.schemas import CartProduct
from repositories import (
    UserRepository,
    CartRepository,
    ProductRepository,
    CartProductRepository,
    OrderRepository
    
)


class OrderService:

    def __init__(self, session:AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.cart_repo = CartRepository(session)
        self.product_repo = ProductRepository(session)
        self.cart_product_repo = CartProductRepository(session)
        self.order_repo = OrderRepository(session)


    async def create_order_id(self,user_id : int):
        # check if cart
        cart = await self.cart_repo.get_cart_by_userid(user_id)

        if not cart:
            raise HTTPException(status_code=404, detail= "cart not found")

        #check if empty or no
        cart_items = await self.cart_product_repo.get_cart_items(cart.id)

        if not cart_items:
            raise HTTPException(status_code=403 , detail = "the cart is empty")

        total = 0
        for item in cart_items:
            product = await self.product_repo.get_product_by_id(item.product_id)

            if not product:
                raise HTTPException(status_code=404 , detail = "product not found")

            if product.stock < item.quantity:
                raise HTTPException(status_code=404 , detail = f"we have only {product.stock} {product.name}")

            total += product.price * item.quantity


        order_db = Order(
            userid = user_id,
            total = total 
        )

       

        try:
            order = await self.order_repo.create_order(order_db)
            await self.order_repo.create_order_products(order.id,cart.id)
            await self.product_repo.decrease_stock_by_cart(cart.id)
            await self.cart_product_repo.delete_items(cart.id)
            await self.session.commit()
            return order
            
        except Exception:
            await self.session.rollback()
            raise

    async def get_order(self,order_id:int):
        order = await self.order_repo.get_order_id(order_id)

        if not order or order.status == orderstatus.cancelled:
            raise HTTPException(status_code = 404 ,detail= "order not found")
        
        order_product = await self.order_repo.get_order_product(order_id)

        return order_product


    
                
    async def cancel_order(self, order_id: int):
        order = await self.order_repo.get_order_id(order_id)
        if not order:
           raise HTTPException(status_code=404, detail="Order not found")

        if order.status == orderstatus.cancelled:
            raise HTTPException(status_code=400, detail="Order already cancelled")

        await self.product_repo.increase_stock_by_order(order_id)
        order.status = orderstatus.cancelled
        await self.session.commit()

        return {"message": "Order cancelled successfully"}
        
        


        


        


        







            


        



       
        


        

        


                