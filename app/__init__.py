from dotenv import load_dotenv
load_dotenv() # para cargar el archivo .env de cada desarrollador

from flask import Flask
from flask_restful import Api
# from app.resources.usuario import UsuarioResource
# from app.resources.localizacion import LocalizacionResource
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
    from app.resources.entrega import EntregaResource, EntregaEstadoResource, EntregasClienteResource


    # Rutas de la API REST
    api.add_resource(AuthResource, '/api/auth/login')
    api.add_resource(AuthRegisterResource, '/api/auth/register')
    # api.add_resource(UsuarioResource, '/api/usuarios/<int:user_id>')
    
    
    api.add_resource(EntregaResource, '/api/entregas')
    api.add_resource(EntregaEstadoResource, '/api/entregas/<int:entrega_id>/estado')
    api.add_resource(EntregasClienteResource, '/api/entregas/mis')
    # api.add_resource(LocalizacionResource, '/api/localizacion')

    return app
