from .motor_client import vote_db
from tornado import gen
from tornado.concurrent import Future

class User:
    collection = vote_db.user

    def __init__(self):
        pass

    # def create(doc):
    #     future = Future()
    #     def handle_insert(result, err):
    #         if err is None
    #             future.set_result(result)
    #         else
    #             future.set_exception(err)
    #     collection.insert(doc, callback=handle_insert)
    #     return future

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value
