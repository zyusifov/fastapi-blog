from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    description: str
    slug: str | None = None
    author_id: int
    created_at: str | None = None