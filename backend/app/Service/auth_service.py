
from app.Model.user import User
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from pwdlib import PasswordHash
from app.Schema.user_schema import UserCreate, UserResponse, UserLogin

from app.Service.jwt_service import create_access_token


"""
Class for basic form of authentation, login will return a JWT token and register will register the user to the database

"""


password_hasher = PasswordHash.recommended()

class AuthService:

    def to_response(self, user:User) -> UserResponse:
            return UserResponse(
                id = str(user.id),
                firstName = user.firstName,
                lastName = user.lastName,
                email = user.email
    
            )
    async def login(self, data: UserLogin):
            existingUser = await User.find_one(User.email == data.email)

            if not existingUser:
                  raise HTTPException(401, "Email Not Found")
            
            existPassword = password_hasher.verify(data.password, existingUser.password_hash)


            if not existPassword:
                  raise HTTPException(401, "Password incorrect")

            token = create_access_token(str(existingUser.id))

            return {
                  "access_token": token,
                  "token_type": "bearer"}
            

    
    async def register(self, data: UserCreate):
            existing = await User.find_one(User.email == data.email)
    
            if existing:
                raise HTTPException(409, "Email already registered")
    
            user = User(
                firstName=data.firstName,
                lastName=data.lastName,
                email=data.email,
                password_hash=password_hasher.hash(data.password)
            )
            try:
                await user.insert()
            except DuplicateKeyError:
                raise HTTPException(409, "Email already registered")
    
            return self.to_response(user)
    


    