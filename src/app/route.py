from tornado.web import url
from handler.signup_handler import SignupHandler

router = [
    url(r"/users", UsersHandler)
]
