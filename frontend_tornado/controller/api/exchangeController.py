import json
from controller.api.commonLoginedController import commonLoginedController

class exchangeControllerList(commonLoginedController):

    def get(self):
        self._initialize()
        self._signcheck({})
        token       = self._token
        response    = self._middleground_get('/api/exchange/list', None, token=token)
        self.finish( json.dumps(response, ensure_ascii=False) )
    
    
    def post(self):
        self.finish( {"code":0, "message":"only GET allowed"} )

