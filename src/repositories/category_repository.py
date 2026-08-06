from modules.db.e_commerce.schemas import Category
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryRepository:
    def __init__(self, session: AsyncSession = None):
        self.session = session


    async def create_category(self, category:Category):
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)

        return category
    


    async def get_category_by_id(self, category_id:int):
        stmt = select(Category).where(Category.id == category_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    

    async def delete_category(self, category_id:int):
        stmt = select(Category).where(Category.id == category_id)
        result = await self.session.execute(stmt)
        
        if result is None:
            return False
        
        

        await self.session.delete(result)
        await self.session.commit()


        return True



