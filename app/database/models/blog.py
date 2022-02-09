from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, event
from database.database import Base
from slugify import slugify


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer , primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    slug = Column(String)
    created_at = Column(DateTime, default=datetime.now())

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and value != oldvalue:
            target.slug = slugify(value)


event.listen(Blog.title, 'set', Blog.generate_slug, retval=False)