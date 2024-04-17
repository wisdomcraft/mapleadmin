from controller.api.commonLoginedController import commonLoginedController

class adminControllerShow(commonLoginedController):

    def get(self):
        self._initialize()
        self._signcheck({})
        token       = self._token
        response    = self._middleground_get('/api/admin/show', None, token=token)
        self.finish(response)
    
    
    def post(self):
        self.finish( {"code":0, "message":"only GET allowed"} )


## ===========================================
class adminControllerUpdate(commonLoginedController):


    def get(self):
        self.finish( {"code":0, "message":"only POST allowed"} )
    
    
    def post(self):
        self._initialize()
        post            = self._post_argument()
        self._signcheck(post)

        admin_password  = post.get('admin_password', None)
        if admin_password == None:
            self.finish( {"code":0, "message":"admin password empty in POST"} )
        if len(admin_password) != 32:
            self.finish( {"code":0, "message":"admin password length is incorrect"} )

        admin_newpassword   = post.get('admin_newpassword', None)
        if admin_newpassword == None:
            self.finish( {"code":0, "message":"admin new password empty in POST"} )
        if len(admin_newpassword) != 32:
            self.finish( {"code":0, "message":"admin new password length is incorrect"} )

        data            = {'admin_password':admin_password, 'admin_newpassword':admin_newpassword}
        token           = self._token
        response        = self._middleground_post('/api/admin/update', data, token=token)
        self.finish(response)
        
