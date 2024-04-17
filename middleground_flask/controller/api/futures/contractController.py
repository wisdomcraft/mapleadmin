from common.httpClass                   import httpClass
from common.mysqlClass                  import mysqlClass
from controller.api.commonController    import commonController


class contractControllerList(commonController):


    def get(self):
        http    = httpClass()
        get     = http.get()
        where   = ''
        '''
        if len(get) > 0:
            where = self.__list_where(get)
        '
        '''
        
        prefix  = self.prefix
        sql     = "select * from `%sfutures_contract` %s order by `contract_code` asc, `contract_product_id` asc" % (prefix, where)

        mysql   = mysqlClass()
        select  = mysql.select(sql)
        if select['code'] !=1:
            return select
        if select['data'] == None:
            return {'code':1, 'message':'', 'data':{'total':0,'rows':None}}
        contract= select['data']

        sql2    = "select * from `%sfutures_product`" % (prefix)
        mysql   = mysqlClass()
        select2 = mysql.select(sql2)
        if select2['code'] !=1:
            return select2
        if select2['data'] == None:
            return {'code':1, 'message':'', 'data':{'total':0,'rows':None}}
        product = select2['data']

        sql3    = "select * from `%sexchange`" % (prefix)
        mysql   = mysqlClass()
        select3 = mysql.select(sql3)
        if select3['code'] !=1:
            return select3
        if select3['data'] == None:
            return {"code":0, "message":"exchange empty"}
        exchange= select3['data']

        for _contract in contract:
            for _product in product:
                if _contract['contract_product_id'] == _product['product_id']:
                    _contract['contract_product_name']      = _product['product_name']
                    _contract['contract_product_class']     = _product['product_class']
            for _exchange in exchange:
                if _contract['contract_exchange_id'] == _exchange['exchange_id']:
                    _contract['contract_exchange_name']     = _exchange['exchange_name']
                    _contract['contract_exchange_shortname']= _exchange['exchange_shortname']

        total   = len(contract)

        result  = {'code':1, 'message':'', 'data':{'total':total,'rows':contract}}
        return result

        
    def post(self):
        return {"code":0, "message":"only GET allowed"}


    '''
    def __list_where(self, data):
        array = []
        for key in data:
            if key == 'contract_product_name':
                prefix  = self.prefix
                sql     = "select * from `%sfutures_product` where `product_name`='%s' limit 1" % (prefix, data[key])
                mysql   = mysqlClass()
                find    = mysql.find(sql)
                if find['code'] != 1:
                    return find;
                if find['data'] == None:
                    resp= Response('{"code":1, "message":"", "data":{"total":0,"rows":null}}')
                    abort(resp)
                array.append("`%s`='%s'" % ('contract_product_id', find['data']['product_id']))
                continue
            array.append("`%s`='%s'" % (key, data[key]))
        where = 'where ' + 'and '.join(array)

        return where;
    '''


## ===========================================
class contractControllerInsert(commonController):


    def get(self):
        return {"code":0, "message":"only POST allowed"}


    def post(self):
        http    = httpClass()
        post    = http.post()

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

        data    = []
        for i in range(0, len(contract_code_list)):
            row = {}
            row['contract_exchange_id'] = contract_exchange_id
            row['contract_product_id']  = contract_product_id
            row['contract_code']        = contract_code_list[i]
            row['contract_name']        = contract_name_list[i]
            row['contract_month']       = contract_month_list[i]
            row['contract_valid']       = contract_valid_list[i]
            data.append(row)
            del row

        mysql   = mysqlClass()
        prefix  = self.prefix
        table   = prefix + 'futures_contract'
        sql     = mysql.multipleListToInsertSql(data, {'table':table, 'ignore':True})
        if sql['code'] !=1:
            return sql
        sql     = sql['data']
        insert  = mysql.insert(sql)
        if insert['code'] !=1:
            return insert

        return {'code':1, 'message':'success'}



