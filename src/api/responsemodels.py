from pydantic import BaseModel, EmailStr

class RegisterResponse(BaseModel):
    id: int
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

class TagResponse(BaseModel):
    name: str

    class Config:
        from_attributes = True

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    uvotec : int
    dvotec : int
    is_open : bool
    author : str
    tags: list[TagResponse]

    class Config:
        from_attributes = True