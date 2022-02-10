from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database.database import Base

from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer , primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now())

    blogs = relationship("Blog", back_populates="creator")