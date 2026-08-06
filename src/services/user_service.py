from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repository import UserRepository
from modules.db.e_commerce.schemas import User,UserRole
from schemas import UserCreateRequest
from fastapi import HTTPException, status



class UserService:

    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)

    async def create_user(self, user_data: UserCreateRequest):

        user = await self.user_repo.get_user_by_email(user_data.email)

        if user:
            if not user.is_deleted:
                
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists"
                       )
            return await self.user_repo.activate_user(user,user_data)

        return await self.user_repo.create_user(user_data)

    async def get_user(self, user_id: int):

        user = await self.user_repo.get_user_by_id(user_id)

        if user is None or user.is_deleted:
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="User not found"
               )
        
        return user
    
    async def update_user(self, user_id: int, user_data: UserCreateRequest):

        user = await self.user_repo.get_user_by_id(user_id)

        if not user or user.is_deleted:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return await self.user_repo.update_user(user, user_data)
    
    async def delete(self,user_id:int):
        user = await self.user_repo.get_user_by_id(user_id)

        if not user or user.is_deleted == True:
            raise HTTPException(status_code=404 , detail= "user not found ")

        success = await self.user_repo.delete_user(user)

        if not success :
            raise HTTPException(status_code=500 , detail= "server error")
        
        return {"message":"the user deleted successfully"}
            


        