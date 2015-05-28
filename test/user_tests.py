import unittest
from app.model.user import User
import motor
from tornado.testing import AsyncTestCase, gen_test
from tornado.web import gen


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

    def test_create(self):
        future = User.create({'username': 'user', 'password': 'pass'})

        def create_callback(f):
            user = f.result()
            self.assertTrue(user.id)
            cursor = User.find({'_id': user.id})

            def each_callback(result, error):
                self.assertFalse(error)
                self.assertEqual(type(result), User)
                self.stop()
            cursor.each(callback=each_callback)

        future.add_done_callback(create_callback)
        self.wait()

    def test_cursor_to_list(self):
        future = User.create({'username': 'user', 'password': 'pass'})

        @gen.coroutine
        def create_callback(f):
            user = f.result()
            cursor = User.find({'_id': user.id})
            users = yield cursor.to_list(1)
            # self.assertEqual(len(users), 1)
            self.stop()

        future.add_done_callback(create_callback)
        self.wait()
