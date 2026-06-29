from datetime import date

from pydantic import BaseModel


class PostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created: date
    updated: date
