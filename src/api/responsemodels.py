from pydantic import BaseModel

class RegisterResponse(BaseModel):
    id: int
    username: str
    email: str