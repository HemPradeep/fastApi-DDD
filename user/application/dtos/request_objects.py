from typing import Literal

from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    user_name: str = Field(pattern=r"[a-zA-Z]+")
    gender: Literal["Male", "Female", "Other"]


class UpdateUserNameRequest(BaseModel):
    user_name: str = Field(pattern=r"[a-zA-Z]+")
