from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base

class Responses(Base):
      __tablename__ = "responses"

      id = Column(Integer, primary_key=True, index=True)
      post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
      admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
      content = Column(Text, nullable=False)
      created_at = Column(DateTime(timezone=True), server_default=func.now())
      post = relationship("Posts", back_populates="responses")
      admin = relationship("Users")