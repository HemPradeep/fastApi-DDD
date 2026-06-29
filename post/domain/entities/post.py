from dataclasses import dataclass
from datetime import date


@dataclass
class Post:
    id: int | None
    author_id: int
    title: str
    content: str
    created: date | None
    updated: date | None
