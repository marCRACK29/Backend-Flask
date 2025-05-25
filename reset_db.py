import os
import shutil
from app import create_app, db
from app.models import *
from flask_migrate import Migrate
from sqlalchemy import text

app = create_app()
migrate = Migrate(app, db)

with app.app_context():
    # Eliminar la carpeta migrations si existe
    if os.path.exists('migrations'):
        shutil.rmtree('migrations')
        print("Carpeta migrations eliminada")
    
    # Eliminar la tabla alembic_version si existe
    try:
        db.session.execute(text('DROP TABLE IF EXISTS alembic_version'))
        db.session.commit()
        print("Tabla alembic_version eliminada")
    except Exception as e:
        print(f"No se pudo eliminar la tabla alembic_version: {e}")
    
    # Eliminar todas las tablas
    db.drop_all()
    print("Tablas eliminadas")
    
    # Crear todas las tablas nuevamente
    db.create_all()
    print("Tablas creadas nuevamente")
    
    print("\nPor favor, ejecuta los siguientes comandos en orden:")
    print("1. flask db init")
    print("2. flask db migrate -m 'initial migration'")
    print("3. flask db upgrade") 