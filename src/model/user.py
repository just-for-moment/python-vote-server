from .motor_client import vote_db
from tornado import gen
from tornado.concurrent import Future

class User
    collection = vote_db.user

    def __init__(self):

    def create(doc):
        future = Future()
        def handle_insert(result, err):
            if err is None
                future.set_result(result)
            else
                future.set_exception(err)
        collection.insert(doc, callback=handle_insert)
        return future

    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
