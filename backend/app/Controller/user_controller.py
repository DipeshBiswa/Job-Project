from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from app.Service.user_service import UserService
from app.Schema.user_schema import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_user_service():
    return UserService()

@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(
    user: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)]
):
    return await service.register(user)

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
