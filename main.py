from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from post.presentation.controllers.post_controller import router as post_router
from shared.infrastructure.database_connection import Database
from user.domain.exceptions.user_exceptions import (
    InvalidUserData,
    InvalidUserName,
    UserNotFound,
)
from user.presentation.controllers.user_controller import router as user_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    yield
    Database.close_connection()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(UserNotFound)
def user_not_found_handler(request: Request, exc: UserNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(InvalidUserData)
def invalid_user_data_handler(request: Request, exc: InvalidUserData) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


@app.exception_handler(InvalidUserName)
def invalid_user_name_handler(request: Request, exc: InvalidUserName) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


app.include_router(user_router, prefix="/api")
app.include_router(post_router, prefix="/api")
