from app import db
from app.models import Envio, Estado, EstadoEnvio
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# No existe un remitente aún al crear un envío
def crear_envio(remitente_id, ruta_id, conductor_id): 
    nuevo_envio = Envio(remitente=remitente_id, ruta=ruta_id, conductor=conductor_id)

    try:
        db.session.add(nuevo_envio)
        db.session.commit()
        return nuevo_envio
    except IntegrityError:
        raise ValueError("No se pudo crear el envío. Verifique que los datos se ingresaron correctamente.")


def actualizar_estado_envio(envio_id, nuevo_estado_id):
    if nuevo_estado_id not in [1,2,3]:
        raise ValueError("El estado debe ser 1 (PREPARACIÓN), 2 (TRÁNSITO) o 3 (ENTREGADO)")
    
    try:
        envio = Envio.query.get(envio_id)
        if not envio:
            raise LookupError(f"Envío con id {envio_id} no encontrado")
        
        nuevo_estado = Estado.query.get(nuevo_estado_id)
        if not nuevo_estado:
            raise LookupError(f"No se encontró el estado con id {nuevo_estado_id}")
        
        nuevo_registro = EstadoEnvio(
            envio = envio,
            estado = nuevo_estado, 
            timestamp = datetime.now(timezone.utc)
        )
        db.session.add(nuevo_registro)
        db.session.commit()

        return {
            "envio_id": envio_id,
            "nuevo_estado": nuevo_estado.estado.value,
            "timestamp": nuevo_registro.timestamp.isoformat()
        }
    
    except SQLAlchemyError as e:
        db.session.rollback()
        print("SQLAlchemy error:", str(e))
        raise RuntimeError("Error al actualizar el estado de la base de datos") from e
    

def obtener_envios_por_usuario(rut_usuario):
    if not isinstance(rut_usuario, str) or len(rut_usuario.strip()) == 0:
        raise ValueError("El RUT del usuario debe ser un string no vacío.")
    
    try:
        envios = Envio.query.filter((Envio.remitente_id == rut_usuario)).all()

        if not envios:
            return None

        return envios

    except Exception as e:
        raise RuntimeError(f"Ocurrió un error al consultar los envíos: {str(e)}")

        
    