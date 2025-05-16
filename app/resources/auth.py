# ESTE ES SOLO UN EJEMPLO. 

from flask_restful import Resource, reqparse
from app.services.auth_service import login_usuario

class AuthResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        return login_usuario(args['email'], args['password'])
