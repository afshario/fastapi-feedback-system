from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UpdateUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    is_active : bool
    

class PostCreate(BaseModel):
    title: str
    content: str
    tags: list[str] = []

class PostUpdate(BaseModel):
    title: str
    content: str
    tags: list[str] = []
    uvotec : int
    dvotec : int
    is_open : bool


class CommentCreate(BaseModel):
    content: str


class VoteType(str, Enum):
    upvote = "up"
    downvote = "down"


class VoteCreate(BaseModel):
    type: VoteType