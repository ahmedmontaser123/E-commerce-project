from fastapi import APIRouter, Depends, HTTPException, logger
from sqlalchemy.ext.asyncio import AsyncSession
from modules.db.database import get_db_session
from schemas import CategoryResponse,CategoryRequest
from repositories import UserRepository,ProductRepository,CategoryRepository
from modules.db.e_commerce.schemas import User,Cart,Product,Category


category_router = APIRouter(
     prefix="/category",
    tags=["category"]
)


@category_router.post("/{user_id}", response_model=CategoryResponse)
async def create_category(
    user_id:int,
    category:CategoryRequest,
    session: AsyncSession = Depends( get_db_session)
):
    user_repo = UserRepository(session)
    user = await user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Only admin users can create products")

    db_cate = Category(
        id = category.id,
        name = category.name
    )


    cate_repo = CategoryRepository(session)
    await cate_repo.create_category(db_cate)
    return db_cate


@category_router.get("/{category_id}", response_model= CategoryResponse)
async def get_category(
    category_id:int,
    session: AsyncSession = Depends(get_db_session)
):
  cate_repo = CategoryRepository(session)
  category = await cate_repo.get_category_by_id(category_id)

  if not category:
        raise HTTPException(status_code=404, detail="Category not found")
  
  return category



@category_router.delete("/{user_id}/{category_id}", response_model = dict)
async def delete_category(
   user_id:int,
   category_id:int,
   session:AsyncSession = Depends(get_db_session)
):
    user_repo = UserRepository(session)
    user = await user_repo.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin users can update products")
    
    cate_repo = CategoryRepository(session)
    success = await cate_repo.delete_category(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}






    
 
   

