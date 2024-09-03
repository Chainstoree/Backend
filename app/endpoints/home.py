from flask_restful import Resource
from app import api

class Home(Resource):
    def get(self):
        return {'message': 'Welcome to our baseurl'}
api.add_resource(Home, '/')