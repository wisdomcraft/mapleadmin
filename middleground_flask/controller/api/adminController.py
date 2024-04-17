import hashlib
from common.httpClass                   import httpClass
from common.mysqlClass                  import mysqlClass
from controller.api.commonController    import commonController

class adminControllerShow(commonController):

    def get(self):
        http    = httpClass()
        admin_id= self.admin_id
        prefix  = self.prefix
        sql     = "select admin_account from `%sadmin` where `admin_id`='%s' limit 1" % (prefix, admin_id)
        mysql   = mysqlClass()
        find    = mysql.find(sql)

        if find['code'] !=1:
            return find
        if find['data'] == None:
            return {'code':0, 'message':'admin not exist'}
        admin   = find['data']

        result  = {'code':1, 'message':'', 'data':admin}
        return result
    
    
    def post(self):
        return {"code":0, "message":"only GET allowed"}


## ===========================================
class adminControllerUpdate(commonController):


    def get(self):
        return {"code":0, "message":"only POST allowed"}
    
    
    def post(self):
        http    = httpClass()
        post    = http.post()

        admin_password      = post.get('admin_password', None)
        if admin_password == None:
            return {"code":0, "message":"admin password empty in POST"}
        if len(admin_password) != 32:
            return {"code":0, "message":"admin password length is incorrect"}

        admin_newpassword   = post.get('admin_newpassword', None)
        if admin_newpassword == None:
            return {"code":0, "message":"admin new password empty in POST"}
        if len(admin_newpassword) != 32:
            return {"code":0, "message":"admin new password length is incorrect"}

        admin_id= self.admin_id

        prefix  = self.prefix
        sql     = "select * from `%sadmin` where `admin_id`='%s' limit 1" % (prefix, admin_id)
        mysql   = mysqlClass()
        find    = mysql.find(sql)

        if find['code'] !=1:
            return find
        if find['data'] == None:
            return {'code':0, 'message':'admin not exist'}
        admin   = find['data']

        if hashlib.md5((admin_password + str(admin['admin_id'])).encode("utf8")).hexdigest() != admin['admin_password']:
            return {'code':0, 'message':'admin password is incorrect'}

        admin_newpassword = hashlib.md5((admin_newpassword + str(admin['admin_id'])).encode("utf8")).hexdigest()
        sql2    = "update `%sadmin` set `admin_password`='%s' where `admin_id`='%s'" % (prefix, admin_newpassword, admin['admin_id'])
        update2 = mysql.set({'host':'master'}).update(sql2)
        if update2['code'] !=1:
            return update2

        result = {'code':1, 'message':''}
        return result

