from tornado.web import RequestHandler

class SignupHandler(RequestHandler)

    def get_current_user(self):
        return self.get_cookie('username')
