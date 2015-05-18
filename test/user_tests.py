import unittest
from app.model.user import User
import motor
from tornado.testing import AsyncTestCase, gen_test


class SimpleUserTestCase(unittest.TestCase):
    def test_constructor(self):
        user = User(username='hello', password='pass')
        self.assertEqual(user.username, 'hello')
        self.assertEqual(user.password, 'pass')

class DBUserTestCase(AsyncTestCase):
    def setUp(self):
        super(DBUserTestCase, self).setUp()
        self.motor_client = motor.MotorClient()
        User.collection = self.motor_client.test.user

    @gen_test
    def test_save(self):
        user = User(username='user', password='pass')
        self.assertEqual(user.is_inserted, False)
        yield user.save()
        self.assertEqual(user.is_inserted, True)
        self.assertTrue(user.id)

        user.username = 'hello'
        yield user.save()
        yield user.save()

    def tearDown(self):
        User.collection.remove()
        self.motor_client.close()
        super(DBUserTestCase, self).tearDown()
