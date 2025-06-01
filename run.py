import eventlet
eventlet.monkey_patch()

import os
from dotenv import load_dotenv
from app import create_app, socketio, db
from app.models import * # Importar los modelos de la base de datos
import app.socketio_events

# Cargar variables de entorno
load_dotenv()

# Inicializar la aplicación
app = create_app()

if __name__ == '__main__':
    # Configurar debug desde variables de entorno
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    # Obtener host y puerto desde variables de entorno o por defecto
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")  # Acepta conexiones externas (requerido por ngrok)
    port = int(os.getenv("FLASK_RUN_PORT", 5000))  # Puerto por defecto de Flask

    print(f"[INFO] SocketIO ejecutando en modo: {socketio.async_mode}")
    socketio.run(app, host=host, port=port, debug=debug)
