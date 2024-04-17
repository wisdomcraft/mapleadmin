import json
from controller.api.commonLoginedController import commonLoginedController

class contractControllerList(commonLoginedController):

    def get(self):
        self._initialize()
        get            = self._get_argument()
        self._signcheck(get)
        token       = self._token
        response    = self._middleground_get('/api/futures/contract/list', get, token=token)
        self.finish( json.dumps(response, ensure_ascii=False) )
    
    
    def post(self):
        self.finish( {"code":0, "message":"only GET allowed"} )


## ===========================================
class contractControllerInsert(commonLoginedController):


    def get(self):
        self.finish( {"code":0, "message":"only POST allowed"} )


    def post(self):
        self._initialize()
        post                = self._post_argument()
        self._signcheck(post)
        
        contract_exchange_id= post.get('contract_exchange_id', None)
        if contract_exchange_id == None:
            return {"code":0, "message":"contract exchange id empty in POST"}
        if ['shfe','zce','dce','cffex','ine'].count(contract_exchange_id) == 0:
            return {"code":0, "message":"contract exchange id is incorrect"}
        
        contract_product_id = post.get('contract_product_id', None)
        if contract_product_id == None:
            return {"code":0, "message":"contract product id empty in POST"}

        contract_code       = post.get('contract_code', None)
        if contract_code == None:
            return {"code":0, "message":"contract code empty in POST"}
        contract_code_list  = contract_code.split(',')
        if len(contract_code_list) == 0:
            return {"code":0, "message":"contract code length is incorrect in POST"}
        for _contract_code in contract_code_list:
            if _contract_code.find(contract_product_id) != 0:
                return {"code":0, "message":"contract code and contract product id are mismatch"}

        contract_name       = post.get('contract_name', None)
        if contract_name == None:
            return {"code":0, "message":"contract name empty in POST"}
        contract_name_list  = contract_name.split(',')
        if len(contract_name_list) == 0:
            return {"code":0, "message":"contrac name length is incorrect in POST"}

        contract_month      = post.get('contract_month', None)
        if contract_month == None:
            return {"code":0, "message":"contract month empty in POST"}
        contract_month_list = contract_month.split(',')
        if len(contract_month_list) == 0:
            return {"code":0, "message":"contrac month length is incorrect in POST"}

        contract_valid      = post.get('contract_valid', None)
        if contract_valid == None:
            return {"code":0, "message":"contract valid empty in POST"}
        contract_valid_list = contract_valid.split(',')
        if len(contract_valid_list) == 0:
            return {"code":0, "message":"contrac valid length is incorrect in POST"}
        for _contract_valid in contract_valid_list:
            if ['0', '1', 0, 1].count(_contract_valid) == 0:
                return {"code":0, "message":"contract valid is incorrect"}

        data                        = {}
        data['contract_exchange_id']= contract_exchange_id
        data['contract_product_id'] = contract_product_id
        data['contract_code']       = contract_code
        data['contract_name']       = contract_name
        data['contract_month']      = contract_month
        data['contract_valid']      = contract_valid

        token       = self._token
        response    = self._middleground_post('/api/futures/contract/insert', data, token=token)
        self.finish(response)
        

