import os
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import jwt

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch

with patch.dict(os.environ, {"JWT_SECRET": "unit-test-secret-key-at-least-32-bytes"}):
    from app.Controller.user_controller import get_auth_service, get_user_service, router

from app.Model.user import User
from app.Service.jwt_service import create_access_token, SECRET_KEY, ALGORITHM
from tests.helpers import LOGIN_DATA, REGISTER_DATA, USER_RESPONSE, USER_ID, make_user


class UserControllerTests(unittest.TestCase):
    def setUp(self):
        # Mount the production router without starting MongoDB's app lifespan.
        app = FastAPI()
        app.include_router(router)
        self.auth = AsyncMock()
        self.users = AsyncMock()
        app.dependency_overrides[get_auth_service] = lambda: self.auth
        app.dependency_overrides[get_user_service] = lambda: self.users
        self.client = self.enterContext(TestClient(app))

    def test_register_returns_201_and_public_user(self):
        self.auth.register.return_value = {**USER_RESPONSE, "password_hash": "private"}
        response = self.client.post("/users/register", json=REGISTER_DATA)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), USER_RESPONSE)
        self.auth.register.assert_awaited_once()
        self.assertEqual(self.auth.register.call_args.args[0].model_dump(), REGISTER_DATA)

    def test_register_returns_409_for_duplicate_email(self):
        self.auth.register.side_effect = HTTPException(409, "Email already registered")
        response = self.client.post("/users/register", json=REGISTER_DATA)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {"detail": "Email already registered"})

    def test_register_rejects_invalid_input_before_calling_service(self):
        invalid_inputs = (
            {**REGISTER_DATA, "email": "invalid"},
            {**REGISTER_DATA, "password": "short"},
            {key: value for key, value in REGISTER_DATA.items() if key != "firstName"},
        )
        for data in invalid_inputs:
            with self.subTest(data=data):
                response = self.client.post("/users/register", json=data)
                self.assertEqual(response.status_code, 422)
        self.auth.register.assert_not_awaited()

    def test_login_sets_authentication_cookie(self):
        token = {"access_token": "test-token", "token_type": "bearer"}
        self.auth.login.return_value = token
        response = self.client.post("/users/login", json=LOGIN_DATA)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Login successful"})
        self.assertEqual(self.client.cookies.get("access_token"), "test-token")
        self.assertIn("HttpOnly", response.headers["set-cookie"])
        self.auth.login.assert_awaited_once()
        self.assertEqual(self.auth.login.call_args.args[0].model_dump(), LOGIN_DATA)

    def test_login_returns_401_for_invalid_credentials(self):
        for detail in ("Email Not Found", "Password incorrect"):
            with self.subTest(detail=detail):
                self.auth.login.side_effect = HTTPException(401, detail)
                response = self.client.post("/users/login", json=LOGIN_DATA)
                self.assertEqual(response.status_code, 401)
                self.assertEqual(response.json(), {"detail": detail})

    def test_login_rejects_invalid_input_before_calling_service(self):
        for data in ({**LOGIN_DATA, "email": "invalid"}, {"email": LOGIN_DATA["email"]}):
            with self.subTest(data=data):
                self.assertEqual(self.client.post("/users/login", json=data).status_code, 422)
        self.auth.login.assert_not_awaited()

    def test_login_cookie_authenticates_me_and_logout_clears_it(self):
        self.auth.login.return_value = {"access_token": create_access_token(USER_ID)}
        self.client.post("/users/login", json=LOGIN_DATA)
        with patch.object(User, "get", new_callable=AsyncMock, return_value=make_user()) as get_user:
            response = self.client.get("/users/me")
        get_user.assert_awaited_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), USER_RESPONSE)
        self.assertEqual(self.client.post("/users/logout").status_code, 200)
        self.assertIsNone(self.client.cookies.get("access_token"))
        self.assertEqual(self.client.get("/users/me").status_code, 401)

    def test_me_returns_401_without_cookie(self):
        response = self.client.get("/users/me")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})

    def test_me_returns_401_for_invalid_or_expired_tokens(self):
        tokens = (
            "malformed-token",
            jwt.encode({"sub": USER_ID, "exp": datetime.now(timezone.utc) - timedelta(minutes=1)}, SECRET_KEY, algorithm=ALGORITHM),
            jwt.encode({"sub": "invalid-user-id", "exp": datetime.now(timezone.utc) + timedelta(minutes=5)}, SECRET_KEY, algorithm=ALGORITHM),
        )
        for token in tokens:
            with self.subTest(token=token):
                self.client.cookies.set("access_token", token)
                response = self.client.get("/users/me")
                self.assertEqual(response.status_code, 401)
                self.assertEqual(response.json(), {"detail": "Invalid or expired token"})

    def test_me_returns_401_when_user_was_deleted(self):
        self.client.cookies.set("access_token", create_access_token(USER_ID))
        with patch.object(User, "get", new_callable=AsyncMock, return_value=None):
            response = self.client.get("/users/me")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "User not found"})
