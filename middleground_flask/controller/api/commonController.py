import hashlib, random, time, json
from flask              import abort, Response
from flask_restful      import Resource
from common.httpClass   import httpClass
from common.mysqlClass  import mysqlClass

class commonController(Resource):

    prefix      = 'maple_'
    token       = None
    admin_id    = None


    def __init__(self):
        http    = httpClass()
        server  = http.server()
        method  = server['REQUEST_METHOD']
        if method != 'GET' and method != 'POST':
            abort(Response('{"code":0, "message":"only GET or POST allowed"}'))

        self.__token()
        self.__admin()

        
##-------------------------------------------
    def __token(self):
        http    = httpClass()
        server  = http.server()
        
        authorization   = server['HTTP_AUTHORIZATION']
        if authorization == None:
            abort(Response('{"code":1300, "message":"Authorization not exist in http header"}'))
            
        authorization   = authorization.split(' ')
        if len(authorization) != 2:
            abort(Response('{"code":1301, "message":"Authorization syntax is incorrect"}'))
        
        self.token      = authorization[1]


##-------------------------------------------
    def __admin(self):
        token   = self.token
        prefix  = self.prefix
        sql     = "select * from `%sadmin_session` where `session_id`='%s' limit 1" % (prefix, token)
        mysql   = mysqlClass()
        find    = mysql.find(sql)
        if find['code'] !=1:
            abort(Response(json.dumps(find, ensure_ascii=False)))
        if find.get('data') == None:
            abort(Response(json.dumps({'code':0, 'message':'not logined'}, ensure_ascii=False)))

        if find['data']['session_expiretime'] < int(time.time()):
            sql2    = "delete from `%sadmin_session` where `session_id`='%s'" % (prefix, token)
            delete2 = mysql.set({'host':'master'}).delete(sql2)
            if delete2['code'] !=1:
                abort(Response(json.dumps(delete2, ensure_ascii=False)))
            abort(Response(json.dumps({'code':1302,'message':'error, token expired, re-login please'}, ensure_ascii=False)))

        sql3    = "update `%sadmin_session` set `session_expiretime`='%s' where `session_id`='%s'" % (prefix, int(time.time())+7200, token)
        update3 = mysql.set({'host':'master'}).update(sql3)
        if update3['code'] !=1:
            abort(Response(json.dumps(update3, ensure_ascii=False)))

        self.admin_id = find['data']['session_admin_id']
