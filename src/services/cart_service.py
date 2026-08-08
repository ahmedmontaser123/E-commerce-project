from sqlalchemy.ext.asyncio import AsyncSession
from modules.db.e_commerce.schemas import User,UserRole
from schemas import UserCreateRequest,CartRequest,CartItemResponse,CartItemRequest,UpdateCartItemRequest
from fastapi import HTTPException, status
from modules.db.e_commerce.schemas import CartProduct
from repositories import (
    UserRepository,
    CartRepository,
    ProductRepository,
    CartProductRepository
)


class CartService:
    def __init__(self, session:AsyncSession):
        self.user_repo = UserRepository(session)
        self.cart_repo = CartRepository(session)
        self.product_repo = ProductRepository(session)
        self.cart_product_repo = CartProductRepository(session)
        

    async def create_cart(self,user_id,cart_data:CartRequest):
        user = await self.user_repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code= 404 , detail= "user not found")
        
        cart = await self.cart_repo.get_cart_by_userid(user_id)

        if cart:
          raise HTTPException(
          status_code=400,
           detail="User already has a cart"
            )
        
        new_cart = await self.cart_repo.create_cart(cart_data)
        
        return new_cart

    async def add_items(self, user_id: int, item: CartItemRequest):
        user = await self.user_repo.get_user_by_id(user_id)
        if user is None or user.is_deleted:
                raise HTTPException(
                       status_code=status.HTTP_404_NOT_FOUND,
                       detail="User not found"
                       )

        cart = await self.cart_repo.get_cart_by_userid(user_id)

        if not cart:
           raise HTTPException(
            status_code=404,
            detail="Cart not found"
             )

    # Get product
        product = await self.product_repo.get_product_by_id(item.product_id)

        if not product:
            raise HTTPException(
            status_code=404,
            detail="Product not found"
            )

        cart_product = await self.cart_product_repo.get_by_cart_and_product(
        cart.id,
        item.product_id
         )

        if cart_product:
            new_quantity = cart_product.quantity + item.quantity

            if new_quantity > product.stock:
               raise HTTPException(
                status_code=400,
                detail=f"Only {product.stock} items available"
                )

            cart_product.quantity = new_quantity
            return await self.cart_product_repo.update(cart_product)

    # Product not in cart
        if item.quantity > product.stock:
            raise HTTPException(
            status_code=400,
            detail=f"Only {product.stock} items available"
            )

        new_item = CartProduct(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity
          )
        

        return await self.cart_product_repo.create(new_item)
    
    async def get_items(self,user_id:int):
        user = await self.user_repo.get_user_by_id(user_id)
        if user is None or user.is_deleted:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
        cart = await self.cart_repo.get_cart_by_userid(user_id)
        if not cart:
            raise HTTPException(
            status_code=404,
            detail="Cart not found"
            )
        
        items = await self.cart_product_repo.get_cart_items(cart.id)

        return items
    
    async def update_quantity(
    self,
    user_id: int,
    item_id: int,
    data: UpdateCartItemRequest
    ):

        user = await self.user_repo.get_user_by_id(user_id)
        if user is None or user.is_deleted:
                   raise HTTPException(
                       status_code=status.HTTP_404_NOT_FOUND,
                       detail="User not found"
                       )
                



        cart = await self.cart_repo.get_cart_by_userid(user_id)

        if not cart:
         raise HTTPException(
            status_code=404,
            detail="Cart not found"
           )

        cart_item = await self.cart_product_repo.get_by_cart_and_product(cart.id,item_id)

        if not cart_item:
           raise HTTPException(
            status_code=404,
            detail="Item not found"
           )

        if cart_item.cart_id != cart.id:
          raise HTTPException(
            status_code=403,
            detail="Item does not belong to this cart"
        )

        product = await self.product_repo.get_product_by_id(
           cart_item.product_id
        )

        if data.quantity > product.stock:
           raise HTTPException(
            status_code=400,
            detail=f"Only {product.stock} items available"
        )

        cart_item.quantity = data.quantity
        return await self.cart_product_repo.update(cart_item)
    
    async def delete_item(
    self,
    user_id: int,
    item_id: int
):
       

      user = await self.user_repo.get_user_by_id(user_id)
      
      if user is None or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
                )
      
      cart = await self.cart_repo.get_cart_by_userid(user_id)

      if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

      cart_item = await self.cart_product_repo.get_by_cart_and_product(cart.id,item_id)

      if not cart_item:
         raise HTTPException(
            status_code=404,
            detail="Item not found"
         )

      if cart_item.cart_id != cart.id:
        raise HTTPException(
            status_code=403,
            detail="Item does not belong to this cart"
        )

      success = await self.cart_product_repo.delete(cart_item)

      if not success:
        raise HTTPException(
            status_code=500,
            detail="internal server error"
        )

      return {
        "message": "Item removed successfully"
        }
    
    async def delete_cart(self, user_id: int):

        cart = await self.cart_repo.get_cart_by_userid(user_id)

        if not cart:
          raise HTTPException(
            status_code=404,
            detail="Cart not found"
           )

        await self.cart_repo.delete_cart(cart)
