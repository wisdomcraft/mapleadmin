# coding=utf-8
import platform

server_develop = ['baizhantianxia']

if platform.node() in server_develop:
    config = {
        'middleground':{
            'host':'127.0.0.1:5080',
        },
        'tornado':{
            'setting':{'debug':True}
        },
        'secret':{
            'key':'mapleadmin'
        }
    }
else:
    config = {}


