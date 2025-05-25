import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import * # Importar los modelos de la base de datos

# cargar las variables de .env
load_dotenv()

app = create_app() # Inicia la aplicación

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Solo para desarrollo
    
    # Solo activar debug si es necesario
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    app.run(debug=debug)
