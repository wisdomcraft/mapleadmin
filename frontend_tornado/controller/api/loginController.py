import json, time, hashlib
import tornado.web
import requests
from controller.api.commonController import commonController


## ===========================================
class loginControllerLogining(commonController):


    def get(self):
        self.write( {"code":0, "message":"only POST allowed"} )
    
    
    def post(self):
        self._initialize()
        post            = self._post_argument()
        #self._signcheck(post)

        admin_account   = post.get('admin_account', None)
        if admin_account == None:
            self.finish( {"code":0, "message":"admin account empty in POST"} )
            return None

        admin_password  = post.get('admin_password', None)
        if admin_password == None:
            self.finish( {"code":0, "message":"admin password empty in POST"} )
            return None
        if len(admin_password) != 32:
            self.finish( {"code":0, "message":"admin password length is incorrect"} )
            return None

        data            = {'admin_account':admin_account, 'admin_password':admin_password}
        response        = self._middleground_post('/api/login/logining', data)
        self.finish(response)


## ===========================================
class loginControllerCheck(commonController):


    def get(self):
        self.write( {"code":0, "message":"only POST allowed"} )
    
    
    def post(self):
        self._initialize()
        self._signcheck({})
        
        authorization   = self.request.headers.get('Authorization', None)
        if authorization == None:
            self.finish( {'code':1300, 'message':'Authorization not exist in http header'} )
            return None
        authorization   = authorization.split( )
        if len(authorization) != 2:
            self.finish( {'code':1301, 'message':'Authorization syntax is incorrect'} )
            return None
        token           = authorization[1]

        response        = self._middleground_post('/api/login/check', None, token=token)
        self.finish(response)


## ===========================================
class loginControllerLogout(commonController):


    def get(self):
        self.write( {"code":0, "message":"only POST allowed"} )
    
    
    def post(self):
        self._initialize()
        self._signcheck({})
        
        authorization   = self.request.headers.get('Authorization', None)
        if authorization == None:
            self.finish( {'code':1300, 'message':'Authorization not exist in http header'} )
            return None
        authorization   = authorization.split( )
        if len(authorization) != 2:
            self.finish( {'code':1301, 'message':'Authorization syntax is incorrect'} )
            return None
        token           = authorization[1]

        response        = self._middleground_post('/api/login/logout', None, token=token)
        self.finish(response)
        