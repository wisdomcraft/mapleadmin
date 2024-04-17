import json
from controller.api.commonLoginedController import commonLoginedController

class productControllerList(commonLoginedController):

    def get(self):
        self._initialize()
        get            = self._get_argument()
        self._signcheck(get)
        token       = self._token
        response    = self._middleground_get('/api/futures/product/list', get, token=token)
        self.finish( json.dumps(response, ensure_ascii=False) )
    
    
    def post(self):
        self.finish( {"code":0, "message":"only GET allowed"} )


## ===========================================
class productControllerInsert(commonLoginedController):


    def get(self):
        self.finish( {"code":0, "message":"only POST allowed"} )


    def post(self):
        self._initialize()
        post                = self._post_argument()
        self._signcheck(post)
        
        product_id          = post.get('product_id', None)
        if product_id == None:
            return '{"code":0, "message":"product_id empty in POST"}'

        product_name        = post.get('product_name', None)
        if product_name == None:
            return '{"code":0, "message":"product_name empty in POST"}'

        product_shortname   = post.get('product_shortname', None)
        if product_shortname == None:
            return '{"code":0, "message":"product_shortname empty in POST"}'

        product_exchange_id = post.get('product_exchange_id', None)
        if product_exchange_id == None:
            return '{"code":0, "message":"product_exchange_id empty in POST"}'

        product_class       = post.get('product_class', None)
        if product_class == None:
            return '{"code":0, "message":"product_class empty in POST"}'

        data                        = {}
        data['product_id']          = product_id
        data['product_name']        = product_name
        data['product_shortname']   = product_shortname
        data['product_exchange_id'] = product_exchange_id
        data['product_class']       = product_class

        token       = self._token
        response    = self._middleground_post('/api/futures/product/insert', data, token=token)
        self.finish(response)
        

