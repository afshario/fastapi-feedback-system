from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
import bcrypt
from sqlalchemy.sql import func
from db import Base

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    is_admin = Column(Boolean , default= False)
    is_active = Column(Boolean , default= False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

    def check_password(self, password: str):
        return bcrypt.checkpw(
            password.encode(),
            self.password.encode()
        )



class AdminProfiles(Base):
    __tablename__ = "admin_profiles"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    Field = Column(String(500))