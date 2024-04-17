import hashlib, random, time
from flask_restful      import Resource
from common.httpClass   import httpClass
from common.mysqlClass  import mysqlClass


class loginControllerLogining(Resource):


    __prefix = 'maple_'


    def get(self):
        return {"code":0, "message":"only POST allowed"}
    
    
    def post(self):
        http    = httpClass()
        post    = http.post()
        
        admin_account   = post.get('admin_account', None)
        if admin_account == None:
            return {"code":0, "message":"admin account empty in POST"}

        admin_password  = post.get('admin_password', None)
        if admin_password == None:
            return {"code":0, "message":"admin password empty in POST"}
        if len(admin_password) != 32:
            return {"code":0, "message":"admin password length is incorrect"}

        prefix  = self.__prefix
        sql     = "select * from `{prefix}admin` where `admin_account`='{admin_account}' limit 1".format(prefix=prefix, admin_account=admin_account)
        mysql   = mysqlClass()
        find    = mysql.find(sql)
        if find['code'] !=1:
            return find
        if find['data'] == None:
            return {'code':0, 'message':'admin account not exist by ' + admin_account}

        admin   = find['data']

        if hashlib.md5((admin_password + str(admin['admin_id'])).encode("utf8")).hexdigest() != admin['admin_password']:
            return {'code':0, 'message':'admin password is incorrect'}

        randomString= random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()') + str(random.randint(0,99999)) + str(time.time())
        session_id  = hashlib.sha1((randomString).encode("utf8")).hexdigest()

        sql2    = "insert into `maple_admin_session` (`session_id`,`session_expiretime`,`session_admin_id`) values ('%s', '%d', '%d')" % (session_id, int(time.time())+7200, admin['admin_id'])
        insert2 = mysql.set({'host':'master'}).insert(sql2)
        if insert2['code'] != 1:
            return insert2

        if random.randint(0,9) == 9:
            sql3    = "delete from `maple_admin_session` where `session_expiretime`<'%s'"
            delete3 = mysql.set({'host':'master'}).delete(sql3, (int(time.time()),))
            if delete3['code'] != 1:
                return delete3

        data    = {'token':session_id, 'field':'/api', 'admin_account':admin_account}
        return {'code':1, 'message':'', 'data':data}


## ===========================================
class loginControllerCheck(Resource):


    __prefix = 'maple_'
    

    def get(self):
        return {"code":0, "message":"only POST allowed"}
    
    
    def post(self):
        http    = httpClass()
        server  = http.server()
        authorization = server['HTTP_AUTHORIZATION']
        if authorization == None:
            return {'code':1300, 'message':'Authorization not exist in http header'}
        authorization = authorization.split( )
        if len(authorization) != 2:
            return {'code':1301, 'message':'Authorization syntax is incorrect'}
        
        token   = authorization[1]

        prefix  = self.__prefix
        sql     = "select * from `%sadmin_session` where `session_id`='%s' limit 1" % (prefix, token)
        mysql   = mysqlClass()
        find    = mysql.find(sql)
        if find['code'] !=1:
            return find
        if find['data'] == None:
            return {'code':0, 'message':'not logined'}

        if find['data']['session_expiretime'] < int(time.time()):
            sql2    = "delete from `%sadmin_session` where `session_id`='%s'" % (prefix, token)
            delete2 = mysql.set({'host':'master'}).delete(sql2)
            if delete2['code'] !=1:
                return delete2
            return {'code':1302,'message':'error, token expired, re-login please'}

        return {'code':1, 'message':'already logined'}


## ===========================================
class loginControllerLogout(Resource):


    __prefix = 'maple_'
    

    def get(self):
        return {"code":0, "message":"only POST allowed"}
    
    
    def post(self):
        http    = httpClass()
        server  = http.server()

        authorization = server['HTTP_AUTHORIZATION']
        if authorization == None:
            return {'code':1300, 'message':'Authorization not exist in http header'}
        authorization = authorization.split( )
        if len(authorization) != 2:
            return {'code':1301, 'message':'Authorization syntax is incorrect'}
        
        token   = authorization[1]

        prefix  = self.__prefix
        mysql   = mysqlClass()
        sql     = "delete from `%sadmin_session` where `session_id`='%s'" % (prefix, token)
        delete  = mysql.set({'host':'master'}).delete(sql)
        if delete['code'] !=1:
            return delete

        return {'code':1, 'message':'logout'}


