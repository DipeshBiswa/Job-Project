import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv

"""
Service class for creating a JWT token 
"""

#loads setting from backend/.env into pythons environment
load_dotenv(Path(__file__).resolve().parents[2] /  ".env")


#get the secret key
SECRET_KEY = os.environ["JWT_SECRET"]

#define algorithm
ALGORITHM = "HS256"

#access token expiration
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "90"))


"""
returns a token to send back to client after logging in 

@Param: user_id (id of the user)
@Return: jwt token
"""
def create_access_token(user_id: str) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": user_id,
        "exp": expiration
    }
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token