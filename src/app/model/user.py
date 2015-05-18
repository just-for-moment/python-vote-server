from .motor_client import motor_client
from tornado import gen
from tornado.concurrent import Future
from motor import MotorCursor

class UserCursor(MotorCursor):

    def __init__(self, Model, cursor, collection):
        self.Model = Model
        super(MotorCursor, self).__init__(cursor, collection)

    def each(self, callback):
        @gen.coroutine
        def create_callback(result, err):
            if err:
                return callback(None, err)
            model = yield self.Model.create(doc)
            callback(model, None)
        super(UserCursor, self).each(callback=create_callback)

class User:
    collection = motor_client.vote_db.user

    def __init__(self, **kwargs):
        self.is_inserted = False
        self.dirty_fields = {}
        self._id = None
        for k in kwargs:
            setattr(self, k, kwargs[k])

    @classmethod
    @gen.coroutine
    def create(ctx, doc):
        """Create the User instance with doc

        :arg dict doc: The key-value pair that used to initialize the new
        instance.
        """
        user = User(**doc)
        yield user.save()
        return user

    @classmethod
    def find(ctx, *args, **kwargs):
        cursor = User.collection.delegate.find(*args, **kwargs)
        return UserCursor(User, cursor, User.collection)

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

    def remove(self):
        if self.id is not None:
            return User.collection.remove({'_id': self.id})

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
