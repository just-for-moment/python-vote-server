from tornado.web import RequestHandler, MissingArgumentError, HTTPError

KEYWORD_ACTIONS = ['login', 'signup']

class KeywordCollisionError(HTTPError):
    pass

class SignupHandler(RequestHandler):
    """handle the user signup action. """
    def post(self):
        try:
            username = self.get_argument('username')
            if username in KEYWORD_ACTIONS:
                raise KeywordCollisionError()
            password = self.get_argument('password')
        except MissingArgumentError:
            self.send_error(403, error="the parameters is not valid")
        except KeywordCollisionError:
            self.send_error(403, error="the username isnot available")
        else:
            self.set_status(200, 'signup successfully!')
            self.set_cookie('username', username)
            self.finish()
