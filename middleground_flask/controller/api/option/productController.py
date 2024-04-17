from common.httpClass                   import httpClass
from common.mysqlClass                  import mysqlClass
from controller.api.commonController    import commonController


class productControllerOptionList(commonController):


    def get(self):
        http    = httpClass()
        get     = http.get()

        prefix  = self.prefix
        sql     = "select * from `%sfutures_option` order by `option_exchange_id` asc" % (prefix)
        mysql   = mysqlClass()
        select  = mysql.select(sql)
        if select['code'] !=1:
            return select
        if select['data'] == None:
            return {'code':1, 'message':'', 'data':{'total':0,'rows':None}}
        option  = select['data']

        sql2    = "select * from `%sexchange`" % (prefix)
        mysql   = mysqlClass()
        select2 = mysql.select(sql2)
        if select2['code'] !=1:
            return select2
        if select2['data'] == None:
            return {"code":0, "message":"exchange empty"}
        exchange= select2['data']

        for _option in option:
            for _exchange in exchange:
                if _option['option_exchange_id'] == _exchange['exchange_id']:
                    _option['option_exchange_name'] = _exchange['exchange_name']

        total   = len(option)

        result  = {'code':1, 'message':'', 'data':{'total':total,'rows':option}}
        return result

        
    def post(self):
        return {"code":0, "message":"only GET allowed"}


