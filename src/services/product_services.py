from sqlalchemy.ext.asyncio import AsyncSession
from modules.db.e_commerce.schemas import *
from schemas import *
from fastapi import HTTPException, status
from modules.db.e_commerce.schemas import CartProduct
from repositories import * 

class ProductService:
    def __init__(self, session:AsyncSession):
        self.product_repo = ProductRepository(session)
        self.user_repo = UserRepository(session)



    async def add_product(self,user_id,product_data:ProductRequest):
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.role != UserRole.Admin:
            raise HTTPException(status_code=403, detail="Only admin users can create products")


        db_product = Product(
            id=product_data.id,
            name=product_data.name,
            stock=product_data.stock,
            price=product_data.price,
            description=product_data.description,
            category_id = product_data.category_id
           )

        await self.product_repo.create_product(db_product)
        return db_product
    
    async def get_product(self, product_id:int):
        product = await self.product_repo.get_product_by_id(product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product

    async def get_all_products(self,skip:int,limit:int):
        products = await self.product_repo.get_all_products(skip, limit)
        return products
        
    async def update_product(self,user_id:int,product_id:int,request:ProductUpdateRequest):
            user = await self.user_repo.get_user_by_id(user_id)
            if not user or user.is_deleted:
                raise HTTPException(status_code=404, detail="User not found")
            if user.role.value != "admin":
                    raise HTTPException(status_code=403, detail="Only admin users can update products")

            product = await self.product_repo.get_product_by_id(product_id)

            if not product:
                    raise HTTPException(status_code=404, detail="Product not found")


            product = await self.product_repo.update_product(product,request)
            if not product:
                raise HTTPException(status_code=404, detail="Product not updated")
            return product

    async def delete_product(self,user_id,product_id):
            user = await self.user_repo.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            if user.role != UserRole.Admin:
                raise HTTPException(status_code=403, detail="Only admin users can delete product")
            
            success = await self.product_repo.delete_product(product_id)

            if not success:
                 raise HTTPException(status_code=404, detail="Product not found")
            
            return {"message": "Product deleted successfully"}
            
    

        
