from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, UniqueConstraint
import enum
from sqlalchemy.sql import func
from src.db import Base

class VoteType(enum.Enum):
    up = "up"
    down = "down"

class Votes(Base):
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    voter = Column(ForeignKey("users.id"))
    post = Column(ForeignKey("posts.id"))
    type = Column(Enum(VoteType))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
        UniqueConstraint("voter", "post", name="unique_voter_post"),
    )