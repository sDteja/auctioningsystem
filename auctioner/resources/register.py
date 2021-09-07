from flask import request
from flask_restful import Resource, reqparse

from models.register import RegisterModel


class Register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('URL', type=str, required=False, help='Optional field')
    parser.add_argument('endpoint', type=str, required=True, help='Required field')

    def post(self):
        request_data = Register.parser.parse_args()
        url = "http://" + request.environ['REMOTE_ADDR'] + ":5000"
        register_url = RegisterModel.find_by_name(url)
        if register_url is None:
            register_bidder = RegisterModel(url, request_data['endpoint'])
            try:
                register_bidder.save_to_db()
            except:
                return {'message': 'An error occurred'}, 500
        return {'message': 'Registered'}, 201


class RegisterList(Resource):

    def get(self):
        result = RegisterModel.find_all()
        if result is not None:
            bidders = [bidder.json() for bidder in result]
            return {'bidders': [bidder_detail['bidder'] for bidder_detail in bidders]}, 200
        return {'message': 'no bidders found'}
