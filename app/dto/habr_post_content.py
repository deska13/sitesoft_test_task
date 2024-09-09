from datetime import datetime

from pydantic import BaseModel


class HabrPostContent(BaseModel):
    """Class for representing Habr post content."""

    title: str
    created_at: datetime | str | None
    url: str
    author: str
    author_url: str
