from .motor_client import vote_db
from tornado import gen
from tornado.concurrent import Future

class User:
    collection = vote_db.user

    def __init__(self, **kwargs):
        @is_inserted = False
        @dirty_fields = {}
        for k in kwargs:
            setattr(self, k, kwargs[k])

    @gen.coroutine
    def create(doc):
        """Create the User instance with doc

        :arg dict doc: The key-value pair that used to initialize the new
        instance.
        """
        user = User(doc)
        yield user.save()
        return user
        
    def save(self):
        """Save the User instance into the db
        """
        try:
            if not self.dirty_fields: # dirty_fields is empty
                future = Future()
                future.set_result(None)
                return future
            else if self.is_inserted:
                self.is_inserted = True
                return collection.update({'_id': self._id}, self.dirty_fields)
            else
                return collection.insert(self.dirty_fields)
        finally:
            self.dirty_fields = {}  # clear the dirty_fields

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
