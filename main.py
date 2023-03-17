from flask import Flask
from flask import request
from flask_restful import Api, Resource
from modules.user import UserModule
from modules.nearby import MapsModule

app = Flask(__name__)
api = Api(app)

count = 0


class Root(Resource):
    def get(self):
        global count
        count += 1
        print(count)
        return {'message': f'Hello from Server [ Count: {count} ]'}


class User(Resource):
    def post(self):
        params = dict(request.values)
        return UserModule.login(params)


class NearByItems(Resource):
    def post(self):
        params = dict(request.values)
        return MapsModule.getNearByItems(params)


class UpsertItems(Resource):
    def post(self):
        params = dict(request.values)
        return MapsModule.insertNewItem(params)


api.add_resource(Root, '/')
api.add_resource(NearByItems, '/nearbyitems')
api.add_resource(UpsertItems, '/updateitems')
api.add_resource(User, '/user')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
