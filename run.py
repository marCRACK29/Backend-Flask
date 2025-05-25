import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import * # Importar los modelos de la base de datos

# Cargar variables de entorno
load_dotenv()

# Inicializar la aplicación
app = create_app()

if __name__ == '__main__':
    # Configurar debug desde variables de entorno
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    app.run(debug=debug)
