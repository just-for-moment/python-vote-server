import unittest
from app.model.user import User
import motor
from tornado.testing import AsyncTestCase, gen_test
from tornado.web import gen
from tornado.concurrent import Future

class SimpleUserTestCase(unittest.TestCase):
    def test_constructor(self):
        user = User({'username': 'hello', 'password': 'pass'})
        self.assertEqual(user.username, 'hello')
        self.assertEqual(user.password, 'pass')


class DBUserTestCase(AsyncTestCase):
    def setUp(self):
        super(DBUserTestCase, self).setUp()
        self.motor_client = motor.MotorClient()
        User.collection = self.motor_client.test.user

    @gen_test
    def test_save(self):
        user = User({'username': 'user', 'password': 'pass'})
        self.assertEqual(user.is_inserted, False)
        yield user.save()
        self.assertEqual(user.is_inserted, True)
        self.assertTrue(user.id)

        user.username = 'hello'
        yield user.save()
        yield user.save()
        yield user.remove()
        return None

    @gen_test
    def test_create(self):
        user = yield User.create({'username': 'user', 'password': 'pass'})
        self.assertTrue(user.id)
        cursor = User.find({'_id': user.id})

        def each_callback(result, error):
            self.assertFalse(error)
        cursor.each(callback=each_callback)

    @gen_test
    def test_cursor_to_list(self):
        user = yield User.create({'username': 'user', 'password': 'pass'})
        cursor = User.find({'_id': user.id})
        users = yield cursor.to_list(1)
        self.assertEqual(len(users), 1)


    @gen_test
    def test_cursor_fetch_next(self):
        user = yield User.create({'username': 'user', 'password': 'pass'})
        cursor = User.find({'_id': user.id})
        yield cursor.fetch_next
        self.assertTrue(cursor.next_object())
