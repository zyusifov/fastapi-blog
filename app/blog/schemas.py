from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    description: str
    slug: str | None = None

class BlogShow(BaseModel):
    title: str
    description: str
    user_id: int
    slug: str | None = None