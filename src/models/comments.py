from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.sql import func
from src.db import Base

class Comments(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    writer = Column(ForeignKey("users.id"))
    post = Column(ForeignKey("posts.id"))
    content = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
        UniqueConstraint("writer", "post", name="unique_comment"),
    )