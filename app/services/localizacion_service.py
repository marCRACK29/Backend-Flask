from app import db
from app.models import Localizacion

def registrar_localizacion(conductor_id, latitud, longitud):
    nueva_localizacion = Localizacion(
        conductor_id=conductor_id,
        latitud=latitud,
        longitud=longitud
    )
    db.session.add(nueva_localizacion)
    db.session.commit()
    return nueva_localizacion

def obtener_ultima_localizacion(conductor_id):
    return Localizacion.query.filter_by(conductor_id=conductor_id).order_by(Localizacion.timestamp.desc()).first()

def obtener_historial_localizaciones(conductor_id):
    return Localizacion.query.filter_by(conductor_id=conductor_id).order_by(Localizacion.timestamp.asc()).all()