
from pydantic import BaseModel, EmailStr, Field


'''
Schema to represent the user that is received from the frontend
'''
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

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str