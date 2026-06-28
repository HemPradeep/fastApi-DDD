from typing import Literal

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    user: str
    gender: Literal["Male", "Female", "Other"]
