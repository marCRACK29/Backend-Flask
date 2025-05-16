from flask import Flask
from flask_restful import Api
from app.resources.auth import AuthResource
# from app.resources.usuario import UsuarioResource
from app.resources.entrega import EntregaResource
# from app.resources.localizacion import LocalizacionResource

def create_app():
    app = Flask(__name__)
    api = Api(app)

    # Rutas de la API REST
    api.add_resource(AuthResource, '/api/auth/login')
    # api.add_resource(UsuarioResource, '/api/usuarios/<int:user_id>')
    api.add_resource(EntregaResource, '/api/entregas/<string:name>')
    # api.add_resource(LocalizacionResource, '/api/localizacion')

    return app
