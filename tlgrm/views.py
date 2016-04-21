from tornado.web import RequestHandler


class IndexView(RequestHandler):
    def get(self):
        self.write('Hello, world')
