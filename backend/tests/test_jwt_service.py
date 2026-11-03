import os
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import jwt

with patch.dict(os.environ, {"JWT_SECRET": "unit-test-secret-key-at-least-32-bytes"}):
    from app.Service import jwt_service

from tests.helpers import USER_ID


class JwtServiceTests(unittest.TestCase):
    def test_token_contains_user_id_and_configured_expiration(self):
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        secret = "unit-test-secret-key-at-least-32-bytes"
        with patch.object(jwt_service, "SECRET_KEY", secret):
            with patch.object(jwt_service, "ACCESS_TOKEN_EXPIRE_MINUTES", 15):
                with patch.object(jwt_service, "datetime") as clock:
                    clock.now.return_value = now
                    token = jwt_service.create_access_token(USER_ID)
        payload = jwt.decode(token, secret, algorithms=["HS256"], options={"verify_exp": False})
        self.assertEqual(payload["sub"], USER_ID)
        self.assertEqual(payload["exp"], int((now + timedelta(minutes=15)).timestamp()))
        with self.assertRaises(jwt.InvalidSignatureError):
            jwt.decode(token, "incorrect-test-secret-at-least-32-bytes", algorithms=["HS256"])
