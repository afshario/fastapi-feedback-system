from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db import Base

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

class Posts(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    author = Column(ForeignKey("users.id"))
    title = Column(String(100),nullable= False,unique= False)
    content = Column(String(500),nullable= False,unique= False)
    uvotec = Column(Integer,nullable= False,unique= False ,default= 0)
    dvotec = Column(Integer,nullable= False,unique= False ,default= 0)
    tags = relationship("Tag",secondary=post_tags, back_populates="posts")
    is_open = Column(Boolean, default= True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())