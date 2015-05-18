import unittest
from app.model.user import User

class TestUser(unittest.TestCase):
    def test_username(self):
        self.user = User()
        self.user.username = 'hello'
        self.assertEqual(self.user.username, 'hello')

    def test_password(self):
        user = User()
        user.password = 'pass'
        self.assertEqual(user.password, 'pass')
