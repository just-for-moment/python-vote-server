from .motor_client import motor_client
from .model_base import ModelBase


class User(ModelBase):
    collection = motor_client.vote_db.user

    def __init__(self, doc):
        super(User, self).__init__(doc)

User.add_attribute('username', 'password')
