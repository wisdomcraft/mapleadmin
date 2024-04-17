# coding=utf-8
from flask import Flask
from flask_restful import Api
from route.route import route

app = Flask(__name__)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
api = Api(app)
route(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5080, debug=True)

