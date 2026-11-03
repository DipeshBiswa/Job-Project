import os
import unittest
from unittest.mock import AsyncMock, patch

from beanie.odm.fields import ExpressionField
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

from app.Model.user import User
from app.Schema.user_schema import UserCreate, UserLogin

with patch.dict(os.environ, {"JWT_SECRET": "unit-test-secret-key-at-least-32-bytes"}):
    from app.Service.auth_service import AuthService, password_hasher

from tests.helpers import LOGIN_DATA, REGISTER_DATA, USER_ID, USER_RESPONSE, make_user


class AuthServiceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.service = AuthService()
        for patcher in (
            patch.object(User, "email", ExpressionField("email"), create=True),
            patch.object(User, "get_pymongo_collection"),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_response_omits_password_hash(self):
        self.assertEqual(self.service.to_response(make_user()).model_dump(), USER_RESPONSE)

    async def test_register_hashes_password_and_inserts_user(self):
        saved = []

        async def insert(user):
            user.id = make_user().id
            saved.append(user)
            return user

        with patch.object(User, "find_one", new_callable=AsyncMock, return_value=None) as find:
            with patch.object(User, "insert", autospec=True, side_effect=insert) as insert_mock:
                response = await self.service.register(UserCreate(**REGISTER_DATA))
        find.assert_awaited_once_with({"email": REGISTER_DATA["email"]})
        insert_mock.assert_awaited_once()
        self.assertEqual(response.model_dump(), USER_RESPONSE)
        self.assertNotEqual(saved[0].password_hash, REGISTER_DATA["password"])
        self.assertTrue(password_hasher.verify(REGISTER_DATA["password"], saved[0].password_hash))

    async def test_register_rejects_existing_email_without_insert(self):
        with patch.object(User, "find_one", new_callable=AsyncMock, return_value=make_user()):
            with patch.object(User, "insert", new_callable=AsyncMock) as insert:
                with self.assertRaises(HTTPException) as raised:
                    await self.service.register(UserCreate(**REGISTER_DATA))
        self.assertEqual(raised.exception.status_code, 409)
        self.assertEqual(raised.exception.detail, "Email already registered")
        insert.assert_not_awaited()

    async def test_register_handles_duplicate_during_insert(self):
        with patch.object(User, "find_one", new_callable=AsyncMock, return_value=None):
            with patch.object(User, "insert", new_callable=AsyncMock, side_effect=DuplicateKeyError("duplicate")):
                with self.assertRaises(HTTPException) as raised:
                    await self.service.register(UserCreate(**REGISTER_DATA))
        self.assertEqual(raised.exception.status_code, 409)
        self.assertEqual(raised.exception.detail, "Email already registered")

    async def test_login_returns_bearer_token(self):
        hashed = password_hasher.hash(LOGIN_DATA["password"])
        with patch.object(User, "find_one", new_callable=AsyncMock, return_value=make_user(password_hash=hashed)) as find:
            with patch("app.Service.auth_service.create_access_token", return_value="test-token") as token:
                response = await self.service.login(UserLogin(**LOGIN_DATA))
        find.assert_awaited_once_with({"email": LOGIN_DATA["email"]})
        token.assert_called_once_with(USER_ID)
        self.assertEqual(response, {"access_token": "test-token", "token_type": "bearer"})

    async def test_login_rejects_unknown_email(self):
        with patch.object(User, "find_one", new_callable=AsyncMock, return_value=None):
            with patch("app.Service.auth_service.create_access_token") as token:
                with self.assertRaises(HTTPException) as raised:
                    await self.service.login(UserLogin(**LOGIN_DATA))
        self.assertEqual(raised.exception.status_code, 401)
        self.assertEqual(raised.exception.detail, "Email Not Found")
        token.assert_not_called()

    async def test_login_rejects_incorrect_password(self):
        hashed = password_hasher.hash("a-different-password")
        with patch.object(User, "find_one", new_callable=AsyncMock, return_value=make_user(password_hash=hashed)):
            with patch("app.Service.auth_service.create_access_token") as token:
                with self.assertRaises(HTTPException) as raised:
                    await self.service.login(UserLogin(**LOGIN_DATA))
        self.assertEqual(raised.exception.status_code, 401)
        self.assertEqual(raised.exception.detail, "Password incorrect")
        token.assert_not_called()
