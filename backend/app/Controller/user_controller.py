from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from app.Service.user_service import UserService
from app.Schema.user_schema import UserCreate, UserResponse,UserLogin, TokenResponse
from app.Service.auth_service import AuthService


'''
Controller to handle the authencation for the user
'''
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

"""
function for return the userService class 
@return: instance of UserService
"""
def get_user_service():
    return UserService()

"""
function for returning the authService class
@return: instance of AuthService
"""
def get_auth_service():
    return AuthService()


"""
controller function to register a user

@return: UserResponse 
"""
@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(
    user: UserCreate,
    service: Annotated[AuthService, Depends(get_auth_service)]
):
    return await service.register(user)

"""
controller function to login the user

@return: token(token to send back to the client)

"""
@router.post("/login", response_model=TokenResponse, status_code=200)
async def login_user(
    user: UserLogin,
    service: Annotated[AuthService, Depends(get_auth_service)]
):
    return await service.login(user)





@router.get("/{email}", response_model=UserResponse)
async def get_user(
    email: str,
    service: Annotated[UserService, Depends(get_user_service)]
):
    user = await service.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code= 404,
            detail="User not found"
        )
    return user
