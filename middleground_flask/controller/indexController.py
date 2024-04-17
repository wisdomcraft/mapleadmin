from flask_restful import Resource

class indexController(Resource):

    def get(self):
        return {'code':0, 'message':'forbidden'}
        
    def post(self):
        return {'code':0, 'message':'forbidden, POST'}

