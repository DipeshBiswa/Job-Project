
from app.Model.user import User
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from pwdlib import PasswordHash
from app.Schema.user_schema import UserCreate, UserResponse

password_hasher = PasswordHash.recommended()

class UserService:

    def to_response(self, user:User) -> UserResponse:
        return UserResponse(
            id = str(user.id),
            firstName = user.firstName,
            lastName = user.lastName,
            email = user.email

        )

    async def get_user_by_email(self,email:str):
        user = await User.find_one(User.email == email)

        if User is None:
            return None
        return self.to_response(User)