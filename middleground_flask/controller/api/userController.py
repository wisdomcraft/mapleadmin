import time
from common.httpClass                   import httpClass
from common.mysqlClass                  import mysqlClass
from controller.api.commonController    import commonController


class userControllerList(commonController):


    def get(self):
        prefix  = self.prefix
        sql     = "select * from `%suser` order by `user_id` desc" % (prefix)
        mysql   = mysqlClass()
        select  = mysql.select(sql)
        if select['code'] !=1:
            return select
        if select['data'] == None:
            return {'code':1, 'message':'', 'data':{'total':0,'rows':None}}
        user    = select['data']

        total   = len(user)

        rows    = []
        for _user in user:
            del _user['user_password']
            _user['user_registertime'] = time.strftime( "%Y-%m-%d %H:%M:%S", time.localtime(_user['user_registertime']) ) + ' GMT+08:00'

        result = {'code':1, 'message':'', 'data':{'total':total,'rows':user}}
        return result
    
    
    def post(self):
        return {"code":0, "message":"only GET allowed"}


