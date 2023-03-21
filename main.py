from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource
from modules.user import UserModule
from modules.nearby import MapsModule
from modules.doctor import DoctorModule
from modules.nurse import NurseModule

app = Flask(__name__)
api = Api(app)
CORS(app)

count = 0


class Root(Resource):
    def get(self):
        global count
        count += 1
        return {'message': f'Hello from Server [ Count: {count} ]'}


class User(Resource):
    def post(self):
        params = dict(request.values)
        return UserModule.login(params)


class UserRegister(Resource):
    def post(self):
        params = dict(request.values)
        return UserModule.create(params)

class Appointment(Resource):
    def post(self):
        params = dict(request.values)
        return UserModule.bookAppointment(params)


class GetAppointment(Resource):
    def post(self):
        params = dict(request.values)
        return UserModule.getAppointment(params)


class DoctorDetails(Resource):
    def post(self):
        params = dict(request.values)
        return DoctorModule.details(params)


class NurseRegister(Resource):
    def post(self):
        params = dict(request.values)
        return NurseModule.create(params)


class NearByItems(Resource):
    def post(self):
        params = dict(request.values)
        return MapsModule.getNearByItems(params)


class InsertItems(Resource):
    def post(self):
        params = dict(request.values)
        return MapsModule.insertNewItem(params)


api.add_resource(Root, '/')
api.add_resource(User, '/userlogin')
api.add_resource(UserRegister, '/user/register')
api.add_resource(Appointment, '/bookappointment')
api.add_resource(GetAppointment, '/getappointment')
api.add_resource(DoctorDetails, '/doctordetails')
api.add_resource(NurseRegister, '/nurse/register')
api.add_resource(NearByItems, '/nearbyitems')
api.add_resource(InsertItems, '/insertitems')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
