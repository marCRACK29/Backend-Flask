from app import db
from app.models import Envio, Estado
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# No existe un remitente aún al crear un envío
def crear_envio(datos):
    try:
        # Crear el estado inicial
        estado_inicial = Estado(estado="preparacion")
        db.session.add(estado_inicial)
        db.session.flush()  # Para obtener el ID del estado

        # Crear el envío
        nuevo_envio = Envio(
            receptor_id=datos.get('receptor_id'),
            remitente_id=datos.get('remitente_id'),
            direccion_origen=datos.get('direccion_origen'),
            direccion_destino=datos.get('direccion_destino'),
            estado_id=estado_inicial.id
        )
        db.session.add(nuevo_envio)
        db.session.commit()
        return nuevo_envio
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e

def actualizar_estado_envio(envio_id, nuevo_estado_str):
    try:
        envio = Envio.query.get_or_404(envio_id)
        estado_actual = envio.estado.estado

        # Validar el nuevo estado
        estados_validos = ["preparacion", "transito", "entregado"]
        if nuevo_estado_str not in estados_validos:
            raise ValueError(f"Estado inválido. Debe ser uno de: {estados_validos}")

        # Validar la transición de estado
        if estado_actual == "entregado":
            raise ValueError("No se puede modificar el estado de un envío entregado")

        if estado_actual == "transito" and nuevo_estado_str == "preparacion":
            raise ValueError("No se puede volver a preparación desde tránsito")

        # Crear nuevo estado
        nuevo_estado = Estado(estado=nuevo_estado_str)
        db.session.add(nuevo_estado)
        db.session.flush()

        # Actualizar el estado del envío
        envio.estado_id = nuevo_estado.id
        db.session.commit()
        return envio
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e

def obtener_envios_por_usuario(rut):
    return Envio.query.filter(
        (Envio.remitente_id == rut) | (Envio.receptor_id == rut)
    ).all()

def obtener_envios_por_conductor(rut):
    return Envio.query.filter_by(conductor_id=rut).all()

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


        
    