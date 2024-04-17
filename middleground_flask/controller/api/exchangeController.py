from common.httpClass                   import httpClass
from common.mysqlClass                  import mysqlClass
from controller.api.commonController    import commonController


class exchangeControllerList(commonController):


    def get(self):
        prefix  = self.prefix
        sql     = "select * from `%sexchange` order by `exchange_sort` asc" % (prefix)
        mysql   = mysqlClass()
        select  = mysql.select(sql)
        if select['code'] !=1:
            return select
        if select['data'] == None:
            return {'code':1, 'message':'', 'data':{'total':0,'rows':None}}

        total   = len(select['data'])

        rows    = []
        for item in select['data']:
            rows.append(item)

        result  = {'code':1, 'message':'', 'data':{'total':total,'rows':rows}}
        return result
    
    
    def post(self):
        return {"code":0, "message":"only GET allowed"}


