from typing import Literal

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    user_name: str
    gender: Literal["Male", "Female", "Other"]
