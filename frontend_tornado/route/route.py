# coding=utf-8
from controller.indexController                 import indexController
from controller.api.loginController             import loginControllerLogining, loginControllerCheck, loginControllerLogout
from controller.api.adminController             import adminControllerShow, adminControllerUpdate
from controller.api.userController              import userControllerList
from controller.api.exchangeController          import exchangeControllerList
from controller.api.futures.productController   import productControllerList, productControllerInsert
from controller.api.futures.contractController  import contractControllerList, contractControllerInsert
from controller.api.futures.snapshotController  import snapshotControllerList
from controller.api.option.productController    import productControllerOptionList


route = [
    (r'/',                      indexController),
    
    (r'/api/login/logining',    loginControllerLogining),
    (r'/api/login/check',       loginControllerCheck),
    (r'/api/login/logout',      loginControllerLogout),
    
    (r'/api/admin/show',        adminControllerShow),
    (r'/api/admin/update',      adminControllerUpdate),
    
    (r'/api/user/list',         userControllerList),
    
    (r'/api/exchange/list',     exchangeControllerList),
    
    (r'/api/futures/product/list',      productControllerList),
    (r'/api/futures/product/insert',    productControllerInsert),
    (r'/api/futures/contract/list',     contractControllerList),
    (r'/api/futures/contract/insert',   contractControllerInsert),
    (r'/api/futures/snapshot/list',     snapshotControllerList),
    
    (r'/api/option/product/list',       productControllerOptionList),
]

