from dotenv import load_dotenv
load_dotenv() # para cargar el archivo .env de cada desarrollador

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# Inicialización de la base de datos (SQLAlchemy)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    api = Api(app)

    # Importar recursos aca para evitar importaciones circulares.
    from app.resources.auth import AuthResource, AuthRegisterResource
    # Rutas de la API REST
    api.add_resource(AuthResource, '/api/auth/login')
    api.add_resource(AuthRegisterResource, '/api/auth/register')
    # api.add_resource(UsuarioResource, '/api/usuarios/<int:user_id>')
    
    from app.resources.entrega import EnvioResource, EnvioEstadoResource, EnviosClienteResource
    api.add_resource(EnvioResource, '/api/envios')
    api.add_resource(EnvioEstadoResource, '/api/envios/<int:envio_id>/estado')
    api.add_resource(EnviosClienteResource, '/api/envios/mis')
    # api.add_resource(LocalizacionResource, '/api/localizacion')

    return app
