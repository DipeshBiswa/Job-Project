from fastapi import HTTPException
from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError

from app.Model.profile import Profile
from app.Schema.profile_schema import ProfileCreate, ProfileResponse


class ProfileService:

    def to_response(self, profile: Profile) -> ProfileResponse:
        return ProfileResponse(
            id=str(profile.id),
            **profile.model_dump(exclude={"id", "userId"})
        )
    async def create_profile(
            self,data:ProfileCreate, userId: PydanticObjectId
    ) -> ProfileResponse:
        existingProfile = await Profile.find_one( Profile.userId == userId)

        if existingProfile:
            raise HTTPException(
                status_code=409,
                detail="Profile already exists"
            )
        profile = Profile(
            userId = userId,
            **data.model_dump()
        )
        try:
            await profile.insert()

        except DuplicateKeyError:
            raise HTTPException(
                status_code=409,
                detail="Profile already exists"
            )
        return self.to_response(profile)

    async def get_profile(
            self,userId: PydanticObjectId
    ) -> ProfileResponse:
        profile = await Profile.find_one(
            Profile.userId == userId
        )

        if profile is None:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )

        return self.to_response(profile)
