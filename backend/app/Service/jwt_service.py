import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] /  ".env")

SECRET_KEY = os.environ["JWT_SECRET"]
ALOGRITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "90"))