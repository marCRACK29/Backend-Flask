import os
from app import create_app, db
from app.models.usuario import Usuario # Importar los modelos de la base de datos
from app.models.entrega_model import EntregaModel

app = create_app() # Inicia la aplicación

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Solo para desarrollo
    
    # Solo activar debug si es necesario
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    app.run(debug=debug)
