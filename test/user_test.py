import unittest
import uuid
from unittest.mock import MagicMock, patch

from app.core.exception import (
    InvaildCredentialsException,
    MismatchPasswordException,
    UserAlreadyExistsException,
    UserNotFoundExeption,
)
from app.core.security import hash_password
from app.models.user import User
from app.service.user import UserService


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.repository = MagicMock()
        self.user_service = UserService(repository=self.repository)

    def test_register_user_success(self):
        email = "test@example.com"
        password = "securepassword123"
        confirm_password = "securepassword123"
        self.repository.user_exists.return_value = False

        def create_user(email_arg, password_hash):
            return User(user_id=uuid.uuid4(), email=email_arg, password_hash=password_hash)

        self.repository.create_user.side_effect = create_user

        with patch('app.service.user.create_access_token', return_value='fake_token') as mock_create_access_token:
            result, token = self.user_service.register_user(email, password, confirm_password)

        self.assertIsInstance(result, User)
        self.assertEqual(token, 'fake_token')
        self.repository.user_exists.assert_called_once_with(email)
        self.repository.create_user.assert_called_once_with(email, result.password_hash)
        mock_create_access_token.assert_called_once_with(user_id=result.user_id)

    def test_register_user_failure_duplicate_email(self):
        email = "test@example.com"
        password = "securepassword123"

        self.repository.user_exists.return_value = True

        with self.assertRaises(UserAlreadyExistsException):
            self.user_service.register_user(email, password, password)

    def test_register_user_failure_mismatch_password(self):
        email = "test@example.com"
        password = "securepassword123"

        self.repository.user_exists.return_value = False

        with self.assertRaises(MismatchPasswordException):
            self.user_service.register_user(email, password, 'wrongpassword')

    def test_login_user_success(self):
        email = "test@example.com"
        password = "securepassword123"
        user = User(user_id=uuid.uuid4(), email=email, password_hash=hash_password(password))

        self.repository.get_user_with_email.return_value = user

        with patch('app.service.user.create_access_token', return_value='fake_token') as mock_create_access_token:
            result, token = self.user_service.login_user(email, password)

        self.assertIsInstance(result, User)
        self.assertEqual(token, 'fake_token')
        self.repository.get_user_with_email.assert_called_once_with(email)
        mock_create_access_token.assert_called_once_with(user_id=user.user_id)

    def test_login_user_failure_user_not_found(self):
        email = "test@example.com"

        self.repository.get_user_with_email.return_value = None

        with self.assertRaises(UserNotFoundExeption):
            self.user_service.login_user(email, 'securepassword123')

    def test_login_user_failure_invalid_credentials(self):
        email = "test@example.com"
        password = "securepassword123"
        user = User(user_id=uuid.uuid4(), email=email, password_hash=hash_password('wrongpassword'))

        self.repository.get_user_with_email.return_value = user

        with self.assertRaises(InvaildCredentialsException):
            self.user_service.login_user(email, password)


if __name__ == '__main__':
    unittest.main()