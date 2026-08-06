from fastapi import APIRouter, Depends, HTTPException, logger,Query
from sqlalchemy.ext.asyncio import AsyncSession
from modules.db.database import get_db_session
from schemas import UserResponse, UserCreateRequest,ProductResponse,ProductUpdateRequest,ProductRequest
from repositories import UserRepository,ProductRepository
from modules.db.e_commerce.schemas import User,Cart,Product
from services import ProductService


product_router = APIRouter(
    prefix="/product",
    tags=["product"]
)


@product_router.post("/{user_id}", response_model=ProductResponse)
async def create_product(
    user_id: int,
    product: ProductRequest,
    session: AsyncSession = Depends(get_db_session)
):
    service = ProductService(session)
    product_db = await service.add_product(user_id,product)
    return product_db

@product_router.get("/", response_model=list[ProductResponse])
async def get_all_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_db_session)
):
    service = ProductService(session)
    products = await service.get_all_products(skip,limit)

    return  products

@product_router.get("/{product_id}", response_model=ProductResponse)
async def get_product_id(
    product_id:int,
    session:AsyncSession = Depends(get_db_session)

):
   service = ProductService(session)
   product = await service.get_product(product_id)

   return product

@product_router.put("/{user_id}/{product_id}", response_model=ProductResponse)
async def update_product(
    user_id: int,
    product_id: int,
    request: ProductUpdateRequest,
    session: AsyncSession = Depends(get_db_session)
):
    service = ProductService(session)
    product = await service.update_product(user_id,product_id,request)
    return product
    
@product_router.delete("/{user_id}/{product_id}", response_model=dict)
async def delete_product(
    user_id: int,
    product_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = ProductService(session)
    success = await service.delete_product(user_id,product_id)
    return success