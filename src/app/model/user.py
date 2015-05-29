from .motor_client import motor_client
from tornado import gen
from tornado.concurrent import Future
from motor import MotorCursor


class UserCursor(MotorCursor):
    def __init__(self, Model, cursor, collection):
        self.Model = Model
        super(MotorCursor, self).__init__(cursor, collection)

    def each(self, callback):
        def create_callback(result, err):
            if err:
                return callback(None, err)
            if result is not None:
                model = self.Model(result)
                callback(model, None)
            else:
                callback(None, None)
        super(UserCursor, self).each(callback=create_callback)

    # @motor_coroutine
    def to_list(self, length=1):
        future = Future()

        @gen.coroutine
        def create_list(docs, err):
            if err:
                return future.set_exception(err)
            list = [self.Model(doc) for doc in docs]
            future.set_result(list)

        super(UserCursor, self).to_list(length, callback=create_list)
        return future

    def next_object(self):
        doc = super(UserCursor, self).next_object()
        return self.Model(doc)


class User:
    collection = motor_client.vote_db.user

    def __init__(self, doc={}):
        self.is_inserted = False
        self.dirty_fields = {}
        self._id = None
        for k in doc:
            setattr(self, k, doc[k])

    @classmethod
    @gen.coroutine
    def create(ctx, doc):
        """Create the User instance with doc

        :arg dict doc: The key-value pair that used to initialize the new
        instance.
        """
        user = User(doc)
        yield user.save()
        return user

    @classmethod
    def find(ctx, *args, **kwargs):
        cursor = User.collection.delegate.find(*args, **kwargs)
        return UserCursor(User, cursor, User.collection)

    @classmethod
    def find_by_id(ctx, id):
        return ctx.find({'_id': id})

    @gen.coroutine
    def save(self):
        """Save the User instance into the db
        """
        collection = User.collection
        if not self.dirty_fields:  # dirty_fields is empty
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

    @classmethod
    def _add_attr(ctx, name):
        prev_name = '_' + name

        def method():
            def fget(self):
                return getattr(self, prev_name)

            def fset(self, value):
                setattr(self, prev_name, value)
            return locals()
        setattr(ctx, name, property(**method()))

    @classmethod
    def add_attribute(ctx, *attrs_def):
        if not hasattr(ctx, 'attrs_def'):
            ctx.attrs_def = {}
        for attr_def in attrs_def:
            if isinstance(attr_def, str):
                name, db_name = attr_def, attr_def
            else:
                name = attr_def['name']
                db_name = attr_def.get('db_name') or name
            ctx.attrs_def[name] = db_name
            ctx._add_attr(name)

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
