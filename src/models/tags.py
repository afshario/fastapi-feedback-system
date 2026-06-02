from sqlalchemy import Column, Integer, String
from db import Base
from models.posts import post_tags, relationship

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    posts = relationship(
        "Posts",
        secondary=post_tags,
        back_populates="tags"
    )