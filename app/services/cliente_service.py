from app import db
from app.models import Cliente
from app.services.envio_service import obtener_envios_por_usuario
from typing import Dict, Any, Optional, List
from sqlalchemy.exc import SQLAlchemyError

def actualizar_direccion(rut_cliente: str, datos_direccion: Dict[str, Any]) -> Dict[str, Any]:
    """
    Actualiza la dirección de un cliente.
    
    Args:
        rut_cliente (str): RUT del cliente
        datos_direccion (Dict[str, Any]): Datos de la dirección a actualizar
        
    Returns:
        Dict[str, Any]: Información del cliente actualizado
        
    Raises:
        ValueError: Si el cliente no existe o los datos son inválidos
        RuntimeError: Si ocurre un error en la base de datos
    """
    try:
        # Validar que el cliente existe
        cliente = Cliente.query.get(rut_cliente)
        if not cliente:
            raise ValueError(f"Cliente con RUT {rut_cliente} no encontrado")
            
        # Validar datos requeridos
        campos_requeridos = ['calle', 'numero_domicilio', 'ciudad', 'region', 'codigo_postal']
        for campo in campos_requeridos:
            if campo not in datos_direccion or not datos_direccion[campo]:
                raise ValueError(f"El campo {campo} es requerido")
        
        # Actualizar dirección
        cliente.calle = datos_direccion['calle']
        cliente.numero_domicilio = datos_direccion['numero_domicilio']
        cliente.ciudad = datos_direccion['ciudad']
        cliente.region = datos_direccion['region']
        cliente.codigo_postal = datos_direccion['codigo_postal']
        
        db.session.commit()
        
        return {
            "rut": cliente.RUT,
            "nombre": cliente.nombre,
            "calle": cliente.calle,
            "numero_domicilio": cliente.numero_domicilio,
            "ciudad": cliente.ciudad,
            "region": cliente.region,
            "codigo_postal": cliente.codigo_postal,
            "correo": cliente.correo
        }
        
    except SQLAlchemyError as e:
        db.session.rollback()
        raise RuntimeError(f"Error al actualizar la dirección: {str(e)}")

def actualizar_correo(rut_cliente: str, nuevo_correo: str) -> Dict[str, Any]:
    """
    Actualiza el correo electrónico de un cliente.
    
    Args:
        rut_cliente (str): RUT del cliente
        nuevo_correo (str): Nuevo correo electrónico del cliente
        
    Returns:
        Dict[str, Any]: Información del cliente actualizado
        
    Raises:
        ValueError: Si el cliente no existe o el correo es inválido
        RuntimeError: Si ocurre un error en la base de datos
    """
    try:
        if not nuevo_correo or len(nuevo_correo.strip()) == 0:
            raise ValueError("El correo no puede estar vacío")
            
        if '@' not in nuevo_correo or '.' not in nuevo_correo:
            raise ValueError("El formato del correo electrónico no es válido")
            
        cliente = Cliente.query.get(rut_cliente)
        if not cliente:
            raise ValueError(f"Cliente con RUT {rut_cliente} no encontrado")
            
        cliente.correo = nuevo_correo
        db.session.commit()
        
        return {
            "rut": cliente.RUT,
            "nombre": cliente.nombre,
            "correo": cliente.correo
        }
        
    except SQLAlchemyError as e:
        db.session.rollback()
        raise RuntimeError(f"Error al actualizar el correo: {str(e)}")

def obtener_envios_cliente(rut_cliente: str) -> Optional[List[Dict[str, Any]]]:
    """
    Obtiene todos los envíos de un cliente (tanto enviados como recibidos).
    
    Args:
        rut_cliente (str): RUT del cliente
        
    Returns:
        Optional[List[Dict[str, Any]]]: Lista de envíos del cliente o None si no hay envíos
    """
    try:
        # Obtener envíos usando el servicio de envíos
        envios = obtener_envios_por_usuario(rut_cliente)
        
        if not envios:
            return None
            
        return [
            {
                "id_envio": envio.id,
                "estado_actual": envio.historial_estados[-1].estado.estado.value if envio.historial_estados else "Sin estado",
                "fecha_ultimo_estado": envio.historial_estados[-1].timestamp.isoformat() if envio.historial_estados else None,
                "remitente": envio.remitente_id,
                "receptor": envio.receptor_id,
                "ruta_id": envio.ruta_id
            }
            for envio in envios
        ]
        
    except Exception as e:
        raise RuntimeError(f"Error al obtener envíos del cliente: {str(e)}")
