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
    
    from app.resources.envio_resources import EnvioResource, EnvioEstadoResource, EnviosClienteResource, EnviosConductorResource
    api.add_resource(EnvioResource, '/api/envios')
    api.add_resource(EnvioEstadoResource, '/api/envios/<int:envio_id>/estado')
    api.add_resource(EnviosClienteResource, '/api/envios/mis')
    api.add_resource(EnviosConductorResource, '/api/envios/conductor')
    
    from app.resources.ruta import RutaResource
    api.add_resource(RutaResource, '/api/rutas')

    from app.resources.localizacion import LocalizacionResource, UltimaLocalizacionResource, HistorialLocalizacionResource
    api.add_resource(LocalizacionResource, '/api/localizacion')
    api.add_resource(UltimaLocalizacionResource, '/api/envios/<int:envio_id>/localizacion')
    api.add_resource(HistorialLocalizacionResource, '/api/envios/<int:envio_id>/historial_localizacion')

    from app.resources.conductor import ConductorEnvioResource, ConductorActualizarEstadoResource
    api.add_resource(ConductorEnvioResource, '/api/conductor/envios/en-curso')
    api.add_resource(ConductorActualizarEstadoResource, '/api/conductor/envios/<int:envio_id>/estado')

    from app.resources.cliente import ClienteDireccionResource, ClienteCorreoResource, ClienteEnviosResource
    api.add_resource(ClienteDireccionResource, '/api/cliente/direccion')
    api.add_resource(ClienteCorreoResource, '/api/cliente/correo')
    api.add_resource(ClienteEnviosResource, '/api/cliente/envios')

    return app
