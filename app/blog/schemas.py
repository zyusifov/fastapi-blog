from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    description: str
    slug: str | None = None
    created_at: str | None = None