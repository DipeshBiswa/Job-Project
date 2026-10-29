
from app.Model.user import User
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from pwdlib import PasswordHash
from app.Schema.user_schema import UserCreate, UserResponse



password_hasher = PasswordHash.recommended()

class AuthService:

    def to_response(self, user:User) -> UserResponse:
            return UserResponse(
                id = str(user.id),
                firstName = user.firstName,
                lastName = user.lastName,
                email = user.email
    
            )
    async def login(self, data: UserCreate):
            existingEmail = await User.find_one(User.email == data.email)

            if not existingEmail:
                  raise HTTPException(409, "Email Not Found")
            
            hashedPassword = password_hasher.hash(data.password)

            existPassword = await User.find_one(User.password_hash == hashedPassword)

            if not existPassword:
                  raise HTTPException(409, "Password incorrect")
            

    
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
    


    