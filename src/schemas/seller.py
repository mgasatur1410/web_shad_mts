from pydantic import BaseModel, Field, EmailStr
from typing import List
from .books import ReturnedBook as BookReturn

# Схема для регистрации продавца (POST)
class SellerCreate(BaseModel):
    first_name: str
    last_name: str
    e_mail: EmailStr
    password: str

# Схема для обновления данных продавца (PUT) – обновлять пароль нельзя
class SellerUpdate(BaseModel):
    first_name: str
    last_name: str
    e_mail: EmailStr

# Схема для возврата данных продавца (GET)
class SellerReturn(BaseModel):
    id: int
    first_name: str
    last_name: str
    e_mail: EmailStr
    books: List[BookReturn] = []  # Список книг, размещённых продавцом

    class Config:
        orm_mode = True
