from pydantic import BaseModel


class CreatePostRequest(BaseModel):
    title: str
    content: str


class UpdatePostRequest(BaseModel):
    title: str
