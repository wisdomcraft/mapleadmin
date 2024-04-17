from controller.api.commonLoginedController import commonLoginedController

class userControllerList(commonLoginedController):

    def get(self):
        self._initialize()
        self._signcheck({})
        token       = self._token
        response    = self._middleground_get('/api/user/list', None, token=token)
        self.finish(response)
    
    
    def post(self):
        self.finish( {"code":0, "message":"only GET allowed"} )

