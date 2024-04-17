# coding=utf-8
import os, json
import tornado.ioloop
import tornado.web
from config import config
from route.route import route


setting = config.get('tornado',{}).get('setting',{})
def make_app():
    return tornado.web.Application(route, **setting)


if __name__ == '__main__':
    app = make_app()
    app.listen(5081)
    tornado.ioloop.IOLoop.current().start()

