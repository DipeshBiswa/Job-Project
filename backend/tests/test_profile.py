import os
import unittest
from unittest.mock import AsyncMock, patch

from beanie import PydanticObjectId
from beanie.odm.fields import ExpressionField
from fastapi.testclient import TestClient
from pymongo.errors import DuplicateKeyError

with patch.dict(os.environ, {"JWT_SECRET": "unit-test-secret-key-at-least-32-bytes"}):
    from app.main import app, lifespan

from app.Dependencies.auth_dependency import get_current_user
from app.Model.profile import Profile
from app.Model.user import User
from tests.helpers import USER_ID, make_user


PROFILE_ID = PydanticObjectId("507f1f77bcf86cd799439012")
PROFILE_DATA = {
    "workExperience": [{"company": "Example", "jobTitle": "Engineer"}],
    "workEligibility": {"requiresSponsorship": True},
}


class ProfileRequestTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.addCleanup(self.client.close)
        app.dependency_overrides[get_current_user] = lambda: make_user()
        self.addCleanup(app.dependency_overrides.pop, get_current_user, None)
        self.enterContext(patch.object(Profile, "userId", ExpressionField("userId"), create=True))
        self.enterContext(patch.object(Profile, "get_pymongo_collection"))
        self.find = self.enterContext(patch.object(Profile, "find_one", new_callable=AsyncMock))
        self.find.return_value = None

    def test_create_then_read_preserves_form_fields(self):
        stored = []

        async def insert(profile):
            profile.id = PROFILE_ID
            stored.append(profile)

        with patch.object(Profile, "insert", new=insert):
            response = self.client.post("/profiles/me", json=PROFILE_DATA)

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["id"], str(PROFILE_ID))
        self.assertEqual(data["workExperience"][0]["company"], "Example")
        self.assertTrue(data["workEligibility"]["requiresSponsorship"])
        self.assertNotIn("userId", data)
        self.assertEqual(stored[0].userId, PydanticObjectId(USER_ID))
        self.find.assert_awaited_once_with({"userId": PydanticObjectId(USER_ID)})

        self.find.return_value = stored[0]
        response = self.client.get("/profiles/me")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)

    def test_existing_profile_returns_conflict(self):
        self.find.return_value = Profile(userId=PydanticObjectId(USER_ID))
        response = self.client.post("/profiles/me", json={})
        self.assertEqual(response.status_code, 409)

    def test_concurrent_duplicate_returns_conflict(self):
        with patch.object(Profile, "insert", new_callable=AsyncMock, side_effect=DuplicateKeyError("duplicate")):
            response = self.client.post("/profiles/me", json={})
        self.assertEqual(response.status_code, 409)

    def test_missing_profile_returns_404(self):
        self.assertEqual(self.client.get("/profiles/me").status_code, 404)

    def test_create_requires_login(self):
        app.dependency_overrides.pop(get_current_user)
        self.assertEqual(self.client.post("/profiles/me", json={}).status_code, 401)


class ProfileStartupTests(unittest.IsolatedAsyncioTestCase):
    async def test_startup_initializes_profile_collection(self):
        with patch("app.main.AsyncMongoClient") as client, patch("app.main.init_beanie", new_callable=AsyncMock) as initialize:
            client.return_value.close = AsyncMock()
            async with lifespan(app):
                self.assertEqual(initialize.call_args.kwargs["document_models"], [User, Profile])
            client.return_value.close.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
