from app import db
from app.models import Localizacion

def registrar_localizacion(envio_id, latitud, longitud):
    nueva_localizacion = Localizacion(
        envio_id=envio_id,
        latitud=latitud,
        longitud=longitud
    )
    db.session.add(nueva_localizacion)
    db.session.commit()
    return nueva_localizacion

def obtener_ultima_localizacion(envio_id):
    return Localizacion.query.filter_by(envio_id=envio_id).order_by(Localizacion.timestamp.desc()).first()

def obtener_historial_localizaciones(envio_id):
    return Localizacion.query.filter_by(envio_id=envio_id).order_by(Localizacion.timestamp.asc()).all()