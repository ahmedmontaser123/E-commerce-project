from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.db.database import get_db_session
from schemas import ReviewRequest, ReviewResponse
from services.review_service import ReviewService

review_router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@review_router.post("/{user_id}", response_model=ReviewResponse, status_code=201)
async def create_review(
    user_id: int,
    request: ReviewRequest,
    session: AsyncSession = Depends(get_db_session)
):
    service = ReviewService(session)
    return await service.create_review(user_id, request)


@review_router.get("/product/{product_id}")
async def get_reviews(
    product_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = ReviewService(session)
    return await service.get_reviews_by_product(product_id)


@review_router.delete("/{user_id}/{review_id}")
async def delete_review(
    user_id: int,
    review_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = ReviewService(session)
    return await service.delete_review(user_id, review_id)
