import json
from controller.api.commonLoginedController import commonLoginedController


class productControllerOptionList(commonLoginedController):

    def get(self):
        self._initialize()
        get            = self._get_argument()
        #self._signcheck(get)
        token       = self._token
        response    = self._middleground_get('/api/option/product/list', get, token=token)
        self.finish( json.dumps(response, ensure_ascii=False) )
    
    
    def post(self):
        self.finish( {"code":0, "message":"only GET allowed"} )

