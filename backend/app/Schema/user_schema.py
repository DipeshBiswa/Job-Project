
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str = Field(min_length = 8)


class UserResponse(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: EmailStr