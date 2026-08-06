
from modules.db.e_commerce.schemas import User
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserCreateRequest,UserUpdateRequest
from datetime import datetime


class UserRepository:

    def __init__(self,session: AsyncSession = None):
        self.session = session

    async def create_user(self, user:UserCreateRequest):

        db_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        role=user.role,
    )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def get_user_by_email(self, email:str):
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id:int):
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()    
    
    async def update_user(
        self,
        user:User,
        user_data:UserUpdateRequest
    ):
        
        user.name = user_data.name
        user.password = user_data.password

        await self.session.commit()
        await self.session.refresh(user)

        return user


    async def activate_user(self,user:User,user_data:UserCreateRequest)->User:
        user.name = user_data.name
        user.password = user_data.password
        user.is_deleted = False
        user.deleted_at = None
        await self.session.commit()
        await self.session.refresh(user)
        return user 


    async def delete_user(
        self,
         user: User,
    ) -> bool:
       
        user.is_deleted = True
        user.deleted_at = datetime.utcnow()
        await self.session.commit()

        return True      


