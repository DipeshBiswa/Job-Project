
from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.Model.user import User
from app.Schema.profile_schema import ProfileCreate, ProfileResponse
from app.Service.profile_service import ProfileService
from app.Dependencies.auth_dependency import get_current_user


router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"]
)

def get_profile_services():
    return ProfileService()


@router.post(
    "/me",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_profile(
    data: ProfileCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ProfileService, Depends(get_profile_services)]
):
    return await service.create_profile(data, current_user.id)

@router.get(
    "/me",
    response_model=ProfileResponse
)
async def get_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ProfileService, Depends(get_profile_services)]
):
    return await service.get_profile(current_user.id)
