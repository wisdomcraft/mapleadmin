from common.httpClass                   import httpClass
from common.mysqlClass                  import mysqlClass
from controller.api.commonController    import commonController


class productControllerList(commonController):


    def get(self):
        http    = httpClass()
        get     = http.get()
        where   = ''
        if len(get) > 0:
            where = self.__list_where(get)

        prefix  = self.prefix
        sql     = "select * from `%sfutures_product` %s order by `product_exchange_id` asc, `product_class` asc, `product_id` asc" % (prefix, where)
        mysql   = mysqlClass()
        select  = mysql.select(sql)
        if select['code'] !=1:
            return select
        if select['data'] == None:
            return {'code':1, 'message':'', 'data':{'total':0,'rows':None}}
        product = select['data']

        sql2    = "select * from `%sexchange`" % (prefix)
        mysql   = mysqlClass()
        select2 = mysql.select(sql2)
        if select2['code'] !=1:
            return select2
        if select2['data'] == None:
            return {"code":0, "message":"exchange empty"}
        exchange= select2['data']

        for _product in product:
            for _exchange in exchange:
                if _product['product_exchange_id'] == _exchange['exchange_id']:
                    _product['product_exchange_name'] = _exchange['exchange_name']

        total   = len(select['data'])

        result = {'code':1, 'message':'', 'data':{'total':total,'rows':product}}
        return result

        
    def post(self):
        return {"code":0, "message":"only GET allowed"}


    def __list_where(self, data):
        array = []
        for key in data:
            array.append("`%s`='%s'" % (key, data[key]))
        where = 'where ' + 'and '.join(array)

        return where;


## ===========================================
class productControllerInsert(commonController):


    def get(self):
        return {"code":0, "message":"only POST allowed"}


    def post(self):
        http    = httpClass()
        post    = http.post()
        product_id          = post.get('product_id', None)
        if product_id == None:
            return {"code":0, "message":"product_id empty in POST"}

        product_name        = post.get('product_name', None)
        if product_name == None:
            return {"code":0, "message":"product_name empty in POST"}

        product_shortname   = post.get('product_shortname', None)
        if product_shortname == None:
            return {"code":0, "message":"product_shortname empty in POST"}

        product_exchange_id = post.get('product_exchange_id', None)
        if product_exchange_id == None:
            return {"code":0, "message":"product_exchange_id empty in POST"}

        product_class       = post.get('product_class', None)
        if product_class == None:
            return {"code":0, "message":"product_class empty in POST"}

        prefix  = self.prefix
        sql     = "select count(*) from `%sfutures_product` where `product_id`='%s'" % (prefix, product_id)
        mysql   = mysqlClass()
        count   = mysql.count(sql)
        if count['code'] !=1:
            return count
        if count['data'] > 0:
            return {'code':0, 'message':'this product already exist by product_id {}'.format(product_id)}

        sql2    = mysql.dictToInsertSql(post, {'table':prefix+'futures_product'});
        if sql2['code'] != 1:
            return sql2
        sql2    = sql2['data']
        insert2 = mysql.insert(sql2)
        if insert2['code'] != 1:
            return insert2

        return {'code':1, 'message':'success'}



