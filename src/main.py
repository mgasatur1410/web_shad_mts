from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.configurations.database import create_db_and_tables, global_init
from src.routers import v1_router
from icecream import ic


@asynccontextmanager
async def lifespan(app: FastAPI):
    ic("I am here!")
    global_init()
    await create_db_and_tables()
    yield


# Приложение FastAPI, которое служит точкой входа
app = FastAPI(
    title="Book Sale Platform App",
    description="Учебное приложение для объявлений о продаже книг",
    version="0.0.1",
    default_response_class=ORJSONResponse,
    responses={404: {"description": "Not found!"}},
    lifespan=lifespan,
)

app.include_router(v1_router)
