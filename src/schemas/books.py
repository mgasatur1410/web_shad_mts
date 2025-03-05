from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError

__all__ = ["IncomingBook", "ReturnedBook", "ReturnedAllbooks"]

# Базовый класс "Книги", содержащий поля, которые есть во всех классах-наследниках.
class BaseBook(BaseModel):
    title: str
    author: str
    year: int

# Класс для валидации входящих данных. Не содержит id, так как его присваивает БД.
class IncomingBook(BaseBook):
    pages: int = Field(default=150, alias="count_pages")
    seller_id: int  # Обязательное поле для связи книги с продавцом

    @field_validator("year")
    @staticmethod
    def validate_year(val: int):
        if val < 2020:
            raise PydanticCustomError("Validation error", "Year is too old!")
        return val

# Класс для валидирования исходящих данных. Он уже содержит id и seller_id.
class ReturnedBook(BaseBook):
    id: int
    pages: int
    seller_id: int

    class Config:
        orm_mode = True

# Класс для возврата массива объектов "Книга"
class ReturnedAllbooks(BaseModel):
    books: list[ReturnedBook]
