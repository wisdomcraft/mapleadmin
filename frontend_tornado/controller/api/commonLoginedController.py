import json, time, hashlib
import requests
from controller.api.commonController import commonController


class commonLoginedController(commonController):


    _token = ''


    def _initialize(self):
        super()._initialize()
        self.__token()


    def __token(self):
        authorization   = self.request.headers.get('Authorization', None)
        if authorization == None:
            self.finish( {'code':1300, 'message':'Authorization not exist in http header'} )
            return None
        authorization   = authorization.split( )
        if len(authorization) != 2:
            self.finish( {'code':1301, 'message':'Authorization syntax is incorrect'} )
            return None
        token           = authorization[1]
        if len(token) == 0:
            self.finish( {'code':0, 'message':'Authorization token empty in http request header'} )
            return None
        self._token     = token


