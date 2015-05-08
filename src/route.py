from tornado.web import url

router = [
    url(r"/signup", SignupHandler)
]
