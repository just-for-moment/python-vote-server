from tornado.web import RequestHandler, MissingArgumentError, HTTPError

KEYWORD_ACTIONS = ['login', 'signup']

class KeywordCollisionError(HTTPError):
    pass

class SignupHandler(RequestHandler)
    """handle the user signup action. """
    def post(self):
        try:
            username = self.get_argument('username')
            if username in KEYWORD_ACTIONS
                raise KeywordCollisionError()
            password = self.get_argument('password')
        except MissingArgumentError
            self.set_status(403, "the parameters is not valid")
            self.finish()
        except KeywordCollisionError
            self.set_status(403, 'the username cannot be available')
            self.finish()
