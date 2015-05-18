from .motor_client import motor_client
from tornado import gen
from tornado.concurrent import Future

class User:
    collection = motor_client.vote_db.user

    def __init__(self, **kwargs):
        self.is_inserted = False
        self.dirty_fields = {}
        for k in kwargs:
            setattr(self, k, kwargs[k])

    @gen.coroutine
    def create(doc):
        """Create the User instance with doc

        :arg dict doc: The key-value pair that used to initialize the new
        instance.
        """
        user = User(**doc)
        yield user.save()
        return user

    @gen.coroutine
    def save(self):
        """Save the User instance into the db
        """
        collection = User.collection
        if not self.dirty_fields: # dirty_fields is empty
            future = Future()
            future.set_result(None)
            return future
        elif self.is_inserted:
            self.dirty_fields = {}  # clear the dirty_fields
            yield collection.update({'_id': self._id}, self.dirty_fields)
        else:
            self.dirty_fields = {}  # clear the dirty_fields
            object_id = yield collection.insert(self.dirty_fields)
            self.is_inserted = True
            self._id = object_id

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self.dirty_fields['username'] = self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self.dirty_fields['password'] = self._password = value
