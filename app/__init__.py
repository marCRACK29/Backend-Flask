from dotenv import load_dotenv
load_dotenv() # para cargar el archivo .env de cada desarrollador

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_socketio import SocketIO
from .config import Config

# Inicialización de extensiones
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*", async_mode='eventlet')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)
    api = Api(app)

    # Importar recursos aca para evitar importaciones circulares.
    from app.resources.auth import AuthResource, AuthRegisterClienteResource, AuthRegisterAdminResource, AuthRegisterConductorResource, LogoutResource, ProfileResource
    api.add_resource(AuthResource, '/api/auth/login')
    api.add_resource(AuthRegisterClienteResource, '/api/auth/register/cliente')
    api.add_resource(AuthRegisterConductorResource, '/api/auth/register/conductor')
    api.add_resource(AuthRegisterAdminResource, '/api/auth/register/admin')
    api.add_resource(LogoutResource, '/logout')
    api.add_resource(ProfileResource, '/profile')
    
    from app.resources.envio_resources import EnvioResource, EnvioEstadoResource, EnviosClienteResource, EnviosConductorResource, EnvioIndividualResource
    api.add_resource(EnvioResource, '/api/envios')
    api.add_resource(EnvioEstadoResource, '/api/envios/<int:envio_id>/estado')
    api.add_resource(EnviosClienteResource, '/api/envios/mis')
    api.add_resource(EnviosConductorResource, '/api/envios/conductor')
    api.add_resource(EnvioIndividualResource, '/api/envios/<int:envio_id>')

    from app.resources.localizacion import LocalizacionResource, UltimaLocalizacionResource, HistorialLocalizacionResource
    api.add_resource(LocalizacionResource, '/api/localizacion')
    api.add_resource(UltimaLocalizacionResource, '/api/envios/<int:envio_id>/localizacion')
    api.add_resource(HistorialLocalizacionResource, '/api/envios/<int:envio_id>/historial_localizacion')

    from app.resources.conductor import ConductorEnvioResource, ConductorActualizarEstadoResource
    api.add_resource(ConductorEnvioResource, '/api/conductor/envios/en-curso')
    api.add_resource(ConductorActualizarEstadoResource, '/api/conductor/envios/<int:envio_id>/estado')

    from app.resources.cliente import ClienteDireccionResource, ClienteCorreoResource, ClienteEnviosResource, ClienteInfoResource
    api.add_resource(ClienteDireccionResource, '/api/cliente/direccion')
    api.add_resource(ClienteCorreoResource, '/api/cliente/correo')
    api.add_resource(ClienteEnviosResource, '/api/cliente/envios')
    api.add_resource(ClienteInfoResource, '/api/cliente/info')

    from app.resources.admin_resource import AsignarConductorResource, ListaConductoresResource, EnviosSinConductorResource
    api.add_resource(AsignarConductorResource, '/api/admin/asignar_conductor/<int:envio_id>')
    api.add_resource(ListaConductoresResource, '/api/admin/conductores')
    api.add_resource(EnviosSinConductorResource, '/api/admin/envios_sin_conductor')


    # Test simple para testear conexión entre frontend y backend
    from app.resources.test_resource import TestConnectionResource
    api.add_resource(TestConnectionResource, '/api/test')

    return app
