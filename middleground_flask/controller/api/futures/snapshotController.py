from common.httpClass                   import httpClass
from common.mysqlClass                  import mysqlClass
from controller.api.commonController    import commonController


class snapshotControllerList(commonController):


    def get(self):
        http    = httpClass()
        get     = http.get()
        
        contract= get.get('contract', None)
        if contract == None:
            return {"code":0, "message":"contract empty in url"}
        del get['contract']

        offset  = 0
        if get.__contains__('offset') == True:
            offset  = int(get['offset'])
            del get['offset']

        limit   = 15
        if get.__contains__('limit') == True:
            limit   = int(get['limit'])
            del get['limit']

        where   = ''
        '''
        if len(get) > 0:
            where = self.__list_where(get)
        '''

        prefix  = self.prefix
        mysql   = mysqlClass()
        sql     = "select count(1) from `%sfutures_%s_snapshot_2021` %s" % (prefix, contract, where)
        count   = mysql.set({'database':'market'}).count(sql)
        if count['code'] !=1:
            return count
        if count['data'] == 0:
            return {'code':1, 'message':'', 'data':{'total':0,'rows':None}}
        total   = count['data']

        sql2    = "select * from `%sfutures_%s_snapshot_2021` %s order by `snapshot_unixtime` desc limit %d, %d" % (prefix, contract, where, offset, limit)
        select2 = mysql.set({'database':'market'}).select(sql2)
        if select2['code'] !=1:
            return select2
        if select2['data'] == None:
            return {'code':1, 'message':'', 'data':{'total':0,'rows':None}}
        data    = select2['data']
        if len(data) > 0:
            for i in range(0, len(data)):
                data[i]['snapshot_datetime']        = data[i]['snapshot_datetime'].strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                snapshot_tradingday                 = str(data[i]['snapshot_tradingday'])
                data[i]['snapshot_tradingday']      = '%s-%s-%s' % (snapshot_tradingday[0:4], snapshot_tradingday[4:6], snapshot_tradingday[6:8])
                data[i]['snapshot_price_average']   = str(data[i]['snapshot_price_average'])
                del snapshot_tradingday

        result  = {'code':1, 'message':'', 'data':{'total':total,'rows':data}}
        return result


    def post(self):
        return {"code":0, "message":"only GET allowed"}


    def __list_where(self, data):
        array = []
        for key in data:
            array.append("`%s`='%s'" % (key, data[key]))
        where = 'where ' + 'and '.join(array)

        return where;

