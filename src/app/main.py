from tornado.ioloop import IOLoop
from tornado.web import Application
from .route import router


def main():
    app = Application(router)
    app.listen(8888)
    IOLoop.current().start()

if __name__ == '__main__':
    main()
