from typing import Annotated, List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.seller import Seller
from src.models.books import Book
from src.schemas.seller import (
    SellerCreate,      # схема для POST (создание продавца)
    SellerUpdate,      # схема для PUT (обновление продавца)
    SellerReturn,      # схема для GET (возврат продавца без пароля)
    BookReturn         # схема для отображения книг продавца
)
from src.configurations import get_async_session

seller_router = APIRouter(tags=["sellers"], prefix="/seller")

DBSession = Annotated[AsyncSession, Depends(get_async_session)]


# 1) POST /api/v1/seller – регистрация продавца
@seller_router.post("/", response_model=SellerReturn, status_code=status.HTTP_201_CREATED)
async def create_seller(
    seller_data: SellerCreate,
    session: DBSession
):
    new_seller = Seller(
        first_name=seller_data.first_name,
        last_name=seller_data.last_name,
        e_mail=seller_data.e_mail,
        password=seller_data.password
    )
    session.add(new_seller)
    await session.flush()
    # Явно обновляем данные продавца, чтобы заполнить поле books
    await session.refresh(new_seller, attribute_names=["books"])
    return new_seller


# 2) GET /api/v1/seller – список всех продавцов (с предварительной загрузкой books)
@seller_router.get("/", response_model=List[SellerReturn])
async def get_sellers(session: DBSession):
    query = select(Seller).options(selectinload(Seller.books))
    result = await session.execute(query)
    sellers = result.scalars().all()
    return sellers


# 3) GET /api/v1/seller/{seller_id} – данные конкретного продавца и его книг
@seller_router.get("/{seller_id}", response_model=SellerReturn)
async def get_seller(seller_id: int, session: DBSession):
    query = select(Seller).options(selectinload(Seller.books)).where(Seller.id == seller_id)
    result = await session.execute(query)
    seller = result.scalar_one_or_none()
    if not seller:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return seller


# 4) PUT /api/v1/seller/{seller_id} – обновление данных продавца (без обновления пароля и книг)
@seller_router.put("/{seller_id}", response_model=SellerReturn)
async def update_seller(
    seller_id: int,
    seller_data: SellerUpdate,
    session: DBSession
):
    seller = await session.get(Seller, seller_id)
    if not seller:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    seller.first_name = seller_data.first_name
    seller.last_name = seller_data.last_name
    seller.e_mail = seller_data.e_mail

    await session.flush()
    await session.refresh(seller, attribute_names=["books"])
    return seller


# 5) DELETE /api/v1/seller/{seller_id} – удаление продавца и всех его книг
@seller_router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(seller_id: int, session: DBSession):
    seller = await session.get(Seller, seller_id)
    if not seller:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await session.delete(seller)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
