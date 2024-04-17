import json
from controller.api.commonLoginedController import commonLoginedController

class snapshotControllerList(commonLoginedController):

    def get(self):
        self._initialize()
        get            = self._get_argument()
        #self._signcheck(get)
        
        contract        = get.get('contract', None)
        if contract == None:
            return {"code":0, "message":"contract empty in GET uri"}
            
        token       = self._token
        response    = self._middleground_get('/api/futures/snapshot/list', get, token=token)
        self.finish( json.dumps(response, ensure_ascii=False) )
    
    
    def post(self):
        self.finish( {"code":0, "message":"only GET allowed"} )

