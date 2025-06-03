from dotenv import load_dotenv
load_dotenv() # para cargar el archivo .env de cada desarrollador

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from flask_cors import CORS

# Inicialización de la base de datos (SQLAlchemy)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)

    # Importar recursos aca para evitar importaciones circulares.
    from app.resources.auth import AuthResource, AuthRegisterClienteResource, AuthRegisterAdminResource, AuthRegisterConductorResource
    api.add_resource(AuthResource, '/api/auth/login')
    api.add_resource(AuthRegisterClienteResource, '/api/auth/register/cliente')
    api.add_resource(AuthRegisterConductorResource, '/api/auth/register/conductor')
    api.add_resource(AuthRegisterAdminResource, '/api/auth/register/admin')
    
    from app.resources.envio_resources import EnvioEstadoResource, EnviosClienteResource, EnviosConductorResource, EnvioResource, AsignarConductorResource, AsignarRutaResource
    api.add_resource(EnvioEstadoResource, '/api/envios/<int:envio_id>/estado')
    api.add_resource(EnviosClienteResource, '/api/envios/mis')
    api.add_resource(EnviosConductorResource, '/api/envios/conductor')
    api.add_resource(EnvioResource, '/api/envios')
    api.add_resource(AsignarConductorResource, "/api/envios/<int:envio_id>/asignar_conductor")
    api.add_resource(AsignarRutaResource, "/api/envios/<int:envio_id>/asignar_ruta")

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

    # Test simple para testear conexión entre frontend y backend
    from app.resources.test_resource import TestConnectionResource
    api.add_resource(TestConnectionResource, '/api/test')

    return app
