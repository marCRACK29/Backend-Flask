from flask_restful import Resource

class TestConnectionResource(Resource):
    def get(self):
        return {'message':'Conexión exitosa entre frontend y backend'}, 200