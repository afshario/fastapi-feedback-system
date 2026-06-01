from pydantic import BaseModel, EmailStr

class RegisterResponse(BaseModel):
    id: int
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr