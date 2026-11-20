from fastapi import Cookie, HTTPException
from beanie import PydanticObjectId

from app.Model.user import User
from app.Service.jwt_service import decode_token


async def get_current_user(
        access_token: str | None = Cookie(defualt=None)
) -> User:
    if not access_token:
        raise HTTPException(401, "Not authenticated")
    try:
        payload = decode_token(access_token)
        user_id = PydanticObjectId(payload["sub"])
    except(ValueError, KeyError):
        raise HTTPException(401, "Invalid or expired token")

    user = await User.get(user_id)

    if user is None:
        raise HTTPException(401, "User not found")

    return user

