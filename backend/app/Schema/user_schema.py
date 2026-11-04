
from pydantic import BaseModel, EmailStr, Field


"""
defines the data the API acceps and returns using pydantic models 

"""


"""
Registration Input
"""
class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str = Field(min_length = 8)

"""
User details returned to the client 
"""
class UserResponse(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: EmailStr

"""
Login Input
"""
class UserLogin(BaseModel):
    email: EmailStr
    password: str

"""
Login Response: access token and token type
"""
class TokenResponse(BaseModel):
    access_token: str
    token_type: str