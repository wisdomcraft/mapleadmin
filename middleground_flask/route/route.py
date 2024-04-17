from controller.indexController                 import indexController
from controller.api.loginController             import loginControllerLogining, loginControllerCheck, loginControllerLogout
from controller.api.adminController             import adminControllerShow, adminControllerUpdate
from controller.api.userController              import userControllerList
from controller.api.exchangeController          import exchangeControllerList
from controller.api.futures.productController   import productControllerList, productControllerInsert
from controller.api.futures.contractController  import contractControllerList, contractControllerInsert
from controller.api.futures.snapshotController  import snapshotControllerList
from controller.api.option.productController    import productControllerOptionList

def route(api):
    api.add_resource(indexController,           '/')
    api.add_resource(loginControllerLogining,   '/api/login/logining')
    api.add_resource(loginControllerCheck,      '/api/login/check')
    api.add_resource(loginControllerLogout,     '/api/login/logout')
    
    api.add_resource(adminControllerShow,       '/api/admin/show')
    api.add_resource(adminControllerUpdate,     '/api/admin/update')
    
    api.add_resource(userControllerList,        '/api/user/list')
    
    api.add_resource(exchangeControllerList,    '/api/exchange/list')
    
    api.add_resource(productControllerList,     '/api/futures/product/list')
    api.add_resource(productControllerInsert,   '/api/futures/product/insert')
    api.add_resource(contractControllerList,    '/api/futures/contract/list')
    api.add_resource(contractControllerInsert,  '/api/futures/contract/insert')
    api.add_resource(snapshotControllerList,    '/api/futures/snapshot/list')

    api.add_resource(productControllerOptionList, '/api/option/product/list')


