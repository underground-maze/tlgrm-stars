import tornado.ioloop

from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.options import options

from tlgrm.settings import app_settings, http_config
from tlgrm.urls import url_patterns


class TlgrmApplication(Application):
    def __init__(self):
        super().__init__(url_patterns, **app_settings)


def main():
    app = TlgrmApplication()
    http_server = HTTPServer(app)
    http_server.listen(**http_config)
    tornado.ioloop.IOLoop.current().start()
