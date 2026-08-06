from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from modules.db.database import get_db_session
from schemas import UserResponse, UserCreateRequest,UserUpdateRequest
from modules.db.e_commerce.schemas import User
from services import UserService


user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@user_router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreateRequest,
    session: AsyncSession = Depends(get_db_session)
):
   
  service = UserService(session)
  result = await service.create_user(user_data)

  return result
  
@user_router.get("/{user_id}", response_model = UserResponse)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = UserService(session)
    user = await service.get_user(user_id)
    return user

@user_router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdateRequest,
    session: AsyncSession = Depends(get_db_session)
):
   service = UserService(session)
   user = await service.update_user(user_id , user_data)
   return user

@user_router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = UserService(session)
    success = await service.delete(user_id)
    return success
    