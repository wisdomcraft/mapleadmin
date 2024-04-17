from flask import Flask, request, abort, Response


class httpClass:


##---------------------------------------
    def server(self):
        REQUEST_METHOD      = request.method;
        CONTENT_TYPE        = request.headers.get('Content-Type', None)
        HTTP_AUTHORIZATION  = request.headers.get('Authorization', None)

        SERVER                      = {}
        SERVER['REQUEST_METHOD']    = REQUEST_METHOD
        SERVER['CONTENT_TYPE']      = CONTENT_TYPE
        SERVER['HTTP_AUTHORIZATION']= HTTP_AUTHORIZATION

        return SERVER


##---------------------------------------
    def get(self):
        argument= request.args
        get     = {}
        for i in argument:
            get[i] = argument[i]
        return get



##---------------------------------------
    def post(self):
        method  = request.method;
        if method != 'POST':
            abort(Response('{"code":0, "message":"only POST allowed for this function"}'))

        type    = request.headers.get('Content-Type', 'application/x-www-form-urlencoded')
        if('application/json' in type): type = 'application/json'

        if type     == 'application/x-www-form-urlencoded':
            return request.form.to_dict()
        elif type   == 'application/json':
            return request.json
        return {}





