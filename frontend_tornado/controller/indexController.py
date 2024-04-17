# coding=utf-8
import tornado.web

class indexController(tornado.web.RequestHandler):
    def get(self):
        self.write({'code':0, 'message':'forbidden'})

