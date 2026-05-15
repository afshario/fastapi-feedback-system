from sqlalchemy import Column, Integer, String
from src.db import Base

class Tags(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    field = Column(String(50), unique=True, nullable=False)