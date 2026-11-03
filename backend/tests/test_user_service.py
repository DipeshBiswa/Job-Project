import unittest
from unittest.mock import AsyncMock, patch

from beanie.odm.fields import ExpressionField

from app.Model.user import User
from app.Service.user_service import UserService
from tests.helpers import USER_RESPONSE, make_user


class UserServiceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.service = UserService()
        self.email_field = patch.object(User, "email", ExpressionField("email"), create=True)
        self.email_field.start()
        self.addCleanup(self.email_field.stop)

    def test_response_omits_password_hash(self):
        self.assertEqual(self.service.to_response(make_user()).model_dump(), USER_RESPONSE)

    async def test_get_user_by_email_returns_matching_user(self):
        with patch.object(User, "find_one", new_callable=AsyncMock, return_value=make_user()) as find:
            response = await self.service.get_user_by_email("test@example.com")
        find.assert_awaited_once_with({"email": "test@example.com"})
        self.assertEqual(response.model_dump(), USER_RESPONSE)

    async def test_get_user_by_email_returns_none_when_missing(self):
        with patch.object(User, "find_one", new_callable=AsyncMock, return_value=None) as find:
            response = await self.service.get_user_by_email("missing@example.com")
        find.assert_awaited_once_with({"email": "missing@example.com"})
        self.assertIsNone(response)
