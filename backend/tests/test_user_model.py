import unittest
from unittest.mock import patch

from pydantic import ValidationError

from app.Model.user import User
from tests.helpers import USER_RESPONSE, make_user


class UserModelTests(unittest.TestCase):
    def test_fields_and_getters(self):
        user = make_user()
        self.assertEqual(user.getFirstName(), USER_RESPONSE["firstName"])
        self.assertEqual(user.getLastName(), USER_RESPONSE["lastName"])
        self.assertEqual(user.getEmail(), USER_RESPONSE["email"])
        self.assertEqual(user.password_hash, "stored-password-hash")

    def test_setters_update_fields(self):
        user = make_user()
        user.setFirstName("New")
        user.setLastName("Name")
        user.setEmail("new@example.com")
        self.assertEqual(user.getFirstName(), "New")
        self.assertEqual(user.getLastName(), "Name")
        self.assertEqual(user.getEmail(), "new@example.com")

    def test_required_fields(self):
        fields = {**USER_RESPONSE, "password_hash": "hash"}
        fields.pop("id")
        for field in fields:
            with self.subTest(field=field):
                with patch.object(User, "get_pymongo_collection"):
                    with self.assertRaises(ValidationError) as raised:
                        User(**{key: value for key, value in fields.items() if key != field})
                self.assertIn(field, [error["loc"][0] for error in raised.exception.errors()])

    def test_collection_name(self):
        self.assertEqual(User.Settings.name, "users")
