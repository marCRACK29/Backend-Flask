from app import db
from app.models import Envio, Estado, EstadoEnvio, Paquete
from app.models.estado import EstadoEnum
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# No existe un remitente aún al crear un envío
# def crear_envio(remitente_id, ruta_id, conductor_id): 
#     nuevo_envio = Envio(remitente_id=remitente_id, ruta_id=ruta_id, conductor_id=conductor_id)

#     try:
#         db.session.add(nuevo_envio)
#         db.session.commit()
#         return nuevo_envio
#     except IntegrityError:
#         raise ValueError("No se pudo crear el envío. Verifique que los datos se ingresaron correctamente.")


def crear_envio_con_paquetes(data):
    envio = Envio(
        remitente_id=data["remitente_id"],
        receptor_id=data["receptor_id"],
        conductor_id=data.get("conductor_id"),
        ruta_id=data.get("ruta_id")
    )

    paquetes_data = data.get("paquetes", [])
    if not paquetes_data:
        raise ValueError("Debes proporcionar al menos un paquete")

    for paquete_info in paquetes_data:
        paquete = Paquete(
            peso=paquete_info["peso"],
            alto=paquete_info.get("alto"),
            largo=paquete_info.get("largo"),
            ancho=paquete_info.get("ancho"),
            descripcion=paquete_info.get("descripcion"),
            envio=envio  # Se vincula el paquete con el envío
        )
        db.session.add(paquete)

    try:
        db.session.add(envio)
        db.session.commit()
        return envio
    except IntegrityError:
        db.session.rollback()
        raise ValueError("No se pudo crear el envío. Verifica los datos ingresados.")



def actualizar_estado_envio(envio_id, nuevo_estado_str):
    try:
        # Validar que el estado sea uno de los permitidos
        try:
            nuevo_estado_enum = EstadoEnum(nuevo_estado_str)
        except ValueError:
            raise ValueError(f"Estado inválido. Debe ser uno de: {[e.value for e in EstadoEnum]}")
        
        envio = Envio.query.get(envio_id)
        if not envio:
            raise LookupError(f"Envío con id {envio_id} no encontrado")
        
        # Obtener el estado actual
        estado_actual = EstadoEnvio.query.filter_by(envio_id=envio_id).order_by(EstadoEnvio.timestamp.desc()).first()
        
        # Validar transición de estado
        if estado_actual:
            estado_actual_enum = estado_actual.estado.estado
            if estado_actual_enum == EstadoEnum.ENTREGADO:
                raise ValueError("No se puede modificar el estado de un envío ya entregado")
            if estado_actual_enum == EstadoEnum.TRANSITO and nuevo_estado_enum == EstadoEnum.PREPARACION:
                raise ValueError("No se puede volver a PREPARACION desde TRANSITO")
        
        # Buscar o crear el estado en la base de datos
        estado_db = Estado.query.filter_by(estado=nuevo_estado_enum).first()
        if not estado_db:
            estado_db = Estado(estado=nuevo_estado_enum)
            db.session.add(estado_db)
        
        nuevo_registro = EstadoEnvio(
            envio = envio,
            estado = estado_db,
            timestamp = datetime.now(timezone.utc)
        )
        db.session.add(nuevo_registro)
        db.session.commit()

        return {
            "envio_id": envio_id,
            "nuevo_estado": nuevo_estado_enum.value,
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

def obtener_envios_por_conductor(conductor_id):
    """
    Obtiene todos los envíos asignados a un conductor específico.
    
    Args:
        conductor_id (str): RUT del conductor
        
    Returns:
        list: Lista de envíos asignados al conductor
    """
    envios = Envio.query.filter_by(conductor_id=conductor_id).all()
    if not envios:
        return None
        
    return envios

        
def asignar_conductor_a_envio(envio_id, rut_conductor):
    envio = Envio.query.get(envio_id)
    if not envio:
        raise ValueError(f"No se encontró el envío con id {envio_id}")

    envio.conductor_id = rut_conductor

    try:
        db.session.commit()
        return envio
    except SQLAlchemyError as e:
        db.session.rollback()
        raise RuntimeError(f"Error al asignar conductor: {str(e)}")


def asignar_ruta_a_envio(envio_id, ruta_id):
    envio = Envio.query.get(envio_id)
    if not envio:
        raise ValueError(f"No se encontró el envío con id {envio_id}")

    envio.ruta_id = ruta_id

    try:
        db.session.commit()
        return envio
    except SQLAlchemyError as e:
        db.session.rollback()
        raise RuntimeError(f"Error al asignar ruta: {str(e)}")

