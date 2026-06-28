from typing import Literal

from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    user: str = Field(pattern=r"[a-zA-Z]+")
    gender: Literal["Male", "Female", "Other"]


class UpdateUserNameRequest(BaseModel):
    user: str = Field(pattern=r"[a-zA-Z]+")
