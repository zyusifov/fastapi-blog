from sqlalchemy import Column, ForeignKey, Integer, String
from database.database import Base


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer , primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    slug = Column(String)
    # created_at = Column(Integer, ForeignKey('user.id'))