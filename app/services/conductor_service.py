from app import db
from app.models.conductor import Conductor
from app.models.envio import Envio
from app.models.estado import Estado
from app.services.envio_service import obtener_envios_por_conductor, actualizar_estado_envio
from typing import Dict, Any
from sqlalchemy.exc import SQLAlchemyError

def obtener_envios_en_curso(conductor_id: str):
    """
    Obtiene los envíos en curso (estado TRANSITO) de un conductor específico.
    
    Args:
        conductor_id (str): RUT del conductor
        
    Returns:
        Optional[List[Dict[str, Any]]]: Lista de envíos en curso o None si no hay envíos
    """
    try:
        # Obtener todos los envíos del conductor usando el servicio de envíos
        envios = obtener_envios_por_conductor(conductor_id)
        
        if not envios:
            return None
            
        envios_en_curso = []
        for envio in envios:
            # Si el envío está en estado TRANSITO, agregarlo a la lista
            if envio.estado == "transito":
                envios_en_curso.append({
                    "id_envio": envio.id,
                    "remitente": envio.remitente_id,
                    "receptor": envio.receptor_id,
                    "ruta_id": envio.ruta_id,
                    "estado_actual": envio.estado
                })
        
        return envios_en_curso if envios_en_curso else None
        
    except Exception as e:
        raise RuntimeError(f"Error al obtener envíos en curso: {str(e)}")

def actualizar_estado_envio_conductor(envio_id: int, conductor_id: str, nuevo_estado_str: str) -> Dict[str, Any]:
    """
    Permite a un conductor actualizar el estado de un envío asignado a él.
    
    Args:
        envio_id (int): ID del envío a actualizar
        conductor_id (str): RUT del conductor que realiza la actualización
        nuevo_estado_str (str): Nuevo estado del envío
        
    Returns:
        Dict[str, Any]: Información del envío actualizado
        
    Raises:
        ValueError: Si el estado es inválido o el conductor no está autorizado
        LookupError: Si el envío no existe
        RuntimeError: Si ocurre un error en la base de datos
    """
    try:
        # Verificar que el envío pertenece al conductor
        envio = Envio.query.get(envio_id)
        if not envio:
            raise LookupError(f"Envío con id {envio_id} no encontrado")
            
        if envio.conductor_id != conductor_id:
            raise ValueError("No tienes autorización para actualizar este envío")
        
        # Usar el servicio de envíos para actualizar el estado
        resultado = actualizar_estado_envio(envio_id, nuevo_estado_str)
        
        # Agregar el conductor_id al resultado
        resultado["conductor_id"] = conductor_id
        
        return resultado
    
    except Exception as e:
        if isinstance(e, (ValueError, LookupError)):
            raise
        raise RuntimeError(f"Error al actualizar el estado del envío: {str(e)}")

def obtener_conductor(rut):
    return Conductor.query.get_or_404(rut)

def obtener_envios_activos_conductor(rut):
    try:
        conductor = Conductor.query.get_or_404(rut)
        envios = Envio.query.filter_by(conductor_id=rut).all()
        
        envios_activos = []
        for envio in envios:
            if envio.estado == "transito":
                envios_activos.append(envio)
        
        return envios_activos
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
