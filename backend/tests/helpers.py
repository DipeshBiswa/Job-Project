"""Database-free fixtures shared by the backend tests."""

from unittest.mock import patch

from beanie import PydanticObjectId

from app.Model.user import User


USER_ID = "507f1f77bcf86cd799439011"
USER_RESPONSE = {
    "id": USER_ID,
    "firstName": "Test",
    "lastName": "User",
    "email": "test@example.com",
}
REGISTER_DATA = {
    "firstName": "Test",
    "lastName": "User",
    "email": "test@example.com",
    "password": "test-password-123",
}
LOGIN_DATA = {"email": REGISTER_DATA["email"], "password": REGISTER_DATA["password"]}


def make_user(**overrides):
    data = {**USER_RESPONSE, "password_hash": "stored-password-hash", **overrides}
    data["id"] = PydanticObjectId(data["id"])
    # Beanie normally checks its collection at construction, even before I/O.
    with patch.object(User, "get_pymongo_collection"):
        return User(**data)
