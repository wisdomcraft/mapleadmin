import json, time, hashlib, urllib.parse
import tornado.web
import requests
from config             import config


class commonController(tornado.web.RequestHandler):


    _host = ''
    
    
    #初始化, 因为构造函数已被占用, 所以又在这里重新定义了一个初始化方法
    def _initialize(self):
        host = config.get('middleground',{}).get('host', '')
        if len(host) == 0:
            self.finish( {"code":0, "message":"middleground host empyt in config"} )
        self._host = host


    #获取GET等操作中, URI中的参数
    def _get_argument(self) -> dict:
        arguments   = self.request.query_arguments
        result      = {}
        for key in arguments:
            result[key] = str(arguments[key][0], 'utf-8')
        return result


    #获取POST等操作中, 请求体中的参数
    def _post_argument(self) -> dict:
        header      = self.request.headers
        content_type= header.get('Content-Type', 'application/x-www-form-urlencoded')
        if 'application/json' in content_type:
            content_type = 'application/json'
        
        result      = {}
        if content_type == 'application/x-www-form-urlencoded':
            arguments   = self.request.body_arguments
            for key in arguments:
                result[key] = str(arguments[key][0], 'utf-8')
        elif content_type == 'application/json':
            json_byte   = self.request.body
            if len(json_byte) > 1:
                result  = json.loads( json_byte.decode('utf8') )
        return result


    #签名验证
    def _signcheck(self, arguments={}):
        if isinstance(arguments, dict) == False:
            self.finish( {'code':0,'message':'error, argument data type is incorrect'} )
        
        secure      = self.request.headers.get('Secure', '')
        if len(secure) < 2:
            self.finish( {"code":0, "message":"Secure empyt in http request header"} )
        secure      = json.loads( secure )

        _timestamp  = secure.get('_timestamp', None)
        if _timestamp == None:
            self.finish( {'code':0,'message':'error, _timestamp empty in argument data'} )
        if isinstance(_timestamp, int):
            _timestamp = str(_timestamp)
        if abs( int(time.time()) - int(_timestamp) ) > 300:
            self.finish( {'code':0,'message':'error, _timestamp is not allowed'} )

        _sign       = secure.get('_sign', None)
        if _sign == None:
            self.finish( {'code':0,'message':'error, _sign empty in argument data'} )

        string      = ''
        if len(arguments) > 0:
            arguments2   = sorted(arguments.items(), key=lambda d:d[0], reverse=False)
            for value2 in arguments2:
                if isinstance(value2[1], str):
                    string  = string + value2[1]
                elif isinstance(value2[1], int):
                    string  = string + str(value2[1])

        key         = config.get('secret',{}).get('key', '')
        if len(key) == 0:
            self.finish( {"code":0, "message":"secret key empyt in config"} )
        
        string      = string + _timestamp + key
        md5         = hashlib.md5(string.encode("utf8")).hexdigest()
        if md5 != _sign:
            self.finish( {'code':0,'message':'error, sign is incorrect'} )


    #访问中台接口的GET封装
    def _middleground_get(self, uri, data, **argument) -> dict:
        host    = self._host
        if len(host) == 0:
            self.finish( {'code':0,'message':'host empty, run _initialize() first or set config'} )
            return None

        header  = {}
        
        string  = ''
        if data!=None and type(data)==type({}) and len(data)>0:
            string = '?' + urllib.parse.urlencode(data)
        
        token   = argument.get('token', None)
        if token != None:
            header['Authorization'] = 'Bearer ' + token
        
        url     = 'http://{host}{uri}{string}' . format(**{'host':host, 'uri':uri, 'string':string})

        try:
            response        = requests.request('GET', url, headers=header)
            if response.status_code != 200:
                self.finish( {'code':0,'message':'visit middleground api failed, response http code {}'}.format(response.status_code) )
                return None
                
            response_json   = response.json()
            if type(response_json) != type({}):
                self.finish( {'code':0,'message':'response json is not dict from middleground api'} )
                return None
                
            return response_json
        except:
            self.finish( {'code':0,'message':'visit middleground api failed by requests'} )
            return None
        
        
    #访问中台接口的POST封装
    def _middleground_post(self, uri, data, **argument) -> dict:
        host    = self._host
        if len(host) == 0:
            self.finish( {'code':0,'message':'host empty, run _initialize() first or set config'} )
            return None

        header  = {}
        
        string  = ''
        if data != None:
            header['Content-Type']  = 'application/json'
            string  = json.dumps(data, ensure_ascii=False)
        
        token   = argument.get('token', None)
        if token != None:
            header['Authorization'] = 'Bearer ' + token
        
        url     = 'http://{host}{uri}' . format(**{'host':host, 'uri':uri})
        
        try:
            response        = requests.request('POST', url, headers=header, data=string.encode('utf-8'))
            
            if response.status_code != 200:
                self.finish( {'code':0,'message':'visit middleground api failed'} )
                
            response_json   = response.json()
            if type(response_json) != type({}):
                self.finish( {'code':0,'message':'response json is not dict from middleground api'} )
                
            return response_json
        except:
            self.finish( {'code':0,'message':'visit middleground api failed by requests'} )
            return None
