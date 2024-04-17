import platform

server_develop = ['baizhantianxia']
server_product = ['my_python_maple_host']

if platform.node() in server_develop:
    config = {
        'mysql':{
            'default':{
                'master':{
                    'host':     '127.0.0.1',
                    'database': 'maplefutures',
                    'user':     'maplefutures_master',
                    'password': '',
                    'port':     33306
                },
                'slave':{
                    'host':     '127.0.0.1',
                    'database': 'maplefutures',
                    'user':     'maplefutures_slave',
                    'password': '',
                    'port':     33306
                }
            },
            'market':{
                'master':{
                    'host':     '127.0.0.1',
                    'database': 'maplefutures_market',
                    'user':     'maplefutures_market_master',
                    'password': '',
                    'port':     33306
                },
                'slave':{
                    'host':     '127.0.0.1',
                    'database': 'maplefutures_market',
                    'user':     'maplefutures_market_slave',
                    'password': '',
                    'port':     33306
                }
            }
        }
    }
elif platform.node() in server_product:
    config = {
        'mysql':{
            'default':{
                'master':{
                    'host':     '172.17.0.1',
                    'database': 'maplefutures',
                    'user':     'maplefutures_master',
                    'password': '',
                    'port':     33306
                },
                'slave':{
                    'host':     '172.17.0.1',
                    'database': 'maplefutures',
                    'user':     'maplefutures_slave',
                    'password': '',
                    'port':     33306
                }
            },
            'market':{
                'master':{
                    'host':     '172.17.0.1',
                    'database': 'maplefutures_market',
                    'user':     'maplefutures_market_master',
                    'password': '',
                    'port':     33306
                },
                'slave':{
                    'host':     '172.17.0.1',
                    'database': 'maplefutures_market',
                    'user':     'maplefutures_market_slave',
                    'password': '',
                    'port':     33306
                }
            }
        }
    }
else:
    config = {}


