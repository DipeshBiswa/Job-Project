import os
import unittest
from unittest.mock import AsyncMock

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch

with patch.dict(os.environ, {"JWT_SECRET": "unit-test-secret-key-at-least-32-bytes"}):
    from app.Controller.user_controller import get_auth_service, get_user_service, router

from tests.helpers import LOGIN_DATA, REGISTER_DATA, USER_RESPONSE


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

    def test_login_returns_200_and_token(self):
        token = {"access_token": "test-token", "token_type": "bearer"}
        self.auth.login.return_value = token
        response = self.client.post("/users/login", json=LOGIN_DATA)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), token)
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

    def test_get_user_returns_public_user(self):
        self.users.get_user_by_email.return_value = {**USER_RESPONSE, "password_hash": "private"}
        response = self.client.get("/users/test@example.com")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), USER_RESPONSE)
        self.users.get_user_by_email.assert_awaited_once_with("test@example.com")

    def test_get_user_returns_404_when_missing(self):
        self.users.get_user_by_email.return_value = None
        response = self.client.get("/users/missing@example.com")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "User not found"})
        self.users.get_user_by_email.assert_awaited_once_with("missing@example.com")
