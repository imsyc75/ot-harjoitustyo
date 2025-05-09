import unittest
from repositories.user_repository import UserRepository
from entities.user import User

user_repository = UserRepository()

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        user_repository.delete_all()

        self.user_test1 = User("testuser1", "password123")
        self.user_test2 = User("testuser2", "password456")

    def test_create(self):
        user_repository.create(self.user_test1)

        found_user = user_repository.find_by_username(self.user_test1.username)
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user["username"], self.user_test1.username)
        self.assertEqual(found_user["password"], self.user_test1.password)

    def test_find_by_username_existing(self):
        user_repository.create(self.user_test1)

        found_user = user_repository.find_by_username(self.user_test1.username)

        self.assertIsNotNone(found_user)
        self.assertEqual(found_user["username"], self.user_test1.username)
        self.assertEqual(found_user["password"], self.user_test1.password)

    def test_find_by_username_non_existing(self):
        found_user = user_repository.find_by_username("nonexistentuser")

        self.assertIsNone(found_user)

if __name__ == '__main__':
    unittest.main()
