from datetime import datetime
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    description: str
    slug: str | None = None
        
    class Config():
        orm_mode = True


class BlogShow(BaseModel):
    title: str
    description: str
    user_id: int
    slug: str | None = None
    created_at: datetime | None = None

    class Config():
        orm_mode = True
