import unittest
from services.user_service import UserService
from repositories.user_repository import UserRepository
from entities.user import User

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_repository = UserRepository()

        self.user_repository.delete_all()

        self.user_service = UserService(self.user_repository)

        self.test_user = User("testuser", "testpassword")

    def test_register_new_user(self):
        result = self.user_service.register("testuser", "testpassword")

        self.assertTrue(result)

        current_user = self.user_service.get_current_user()
        self.assertIsNotNone(current_user)
        self.assertEqual(current_user.username, "testuser")
        self.assertEqual(current_user.password, "testpassword")

    def test_register_with_empty_credentials(self):

        result1 = self.user_service.register("", "testpassword")
        self.assertFalse(result1)

        result2 = self.user_service.register("testuser", "")
        self.assertFalse(result2)

    def test_register_existing_user(self):
        self.user_service.register("testuser", "testpassword")

        result = self.user_service.register("testuser", "newpassword")

        self.assertFalse(result)

    def test_login_correct_credentials(self):
        self.user_service.register("testuser", "testpassword")
        self.user_service.logout()

        result = self.user_service.login("testuser", "testpassword")

        self.assertTrue(result)

        current_user = self.user_service.get_current_user()
        self.assertIsNotNone(current_user)
        self.assertEqual(current_user.username, "testuser")

    def test_login_nonexistent_user(self):
        result = self.user_service.login("nonexistent", "password")

        self.assertFalse(result)
        self.assertIsNone(self.user_service.get_current_user())

    def test_login_incorrect_password(self):
        self.user_service.register("testuser", "testpassword")
        self.user_service.logout()

        result = self.user_service.login("testuser", "wrongpassword")

        self.assertFalse(result)
        self.assertIsNone(self.user_service.get_current_user())

    def test_logout(self):
        self.user_service.register("testuser", "testpassword")

        result = self.user_service.logout()

        self.assertTrue(result)

        self.assertIsNone(self.user_service.get_current_user())

    def test_get_current_user_when_logged_in(self):
        self.user_service.register("testuser", "testpassword")

        current_user = self.user_service.get_current_user()

        self.assertIsNotNone(current_user)

        self.assertEqual(current_user.username, "testuser")
        self.assertEqual(current_user.password, "testpassword")

    def test_get_current_user_when_not_logged_in(self):
        self.user_service.logout()

        current_user = self.user_service.get_current_user()

        self.assertIsNone(current_user)

    def test_register_when_create_fails(self):
        class FailingCreateUserRepository(UserRepository):
            # se on erityinen UserRepository-aliluokka
            def create(self, user):
                if user.username == "fail_create_user":
                    return False
                return super().create(user)

        failing_repository = FailingCreateUserRepository()
        user_service = UserService(failing_repository)

        result = user_service.register("fail_create_user", "testpassword")

        self.assertFalse(result)
        self.assertIsNone(user_service.get_current_user())

if __name__ == '__main__':
    unittest.main()
