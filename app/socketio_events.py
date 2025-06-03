from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room
from app import socketio
from datetime import datetime
from app import db
from app.models import *
from sqlalchemy import and_, or_

@socketio.on('connect')
def handle_connect():
    print(f'Cliente conectado: {request.sid}')
    emit('connected', {'message': 'Conectado al servidor de tracking'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Cliente desconectado: {request.sid}')

@socketio.on('join_tracking')
def handle_join_tracking(data):
    print(f'🔵 Evento join_tracking recibido: {data}')
    
    envio_id = data.get('envio_id')
    user_type = data.get('user_type')
    user_id = data.get('user_id')
    
    if verificar_permiso_seguimiento(envio_id, user_id, user_type):
        print(f'✅ Permiso concedido para seguimiento del envío {envio_id} por {user_type} {user_id}')
        join_room(f'envio_{envio_id}')

        estado_actual = get_envio_status(envio_id)
        print(f'📤 Enviando estado actual: {estado_actual}')

        emit('joined_tracking', {
            'envio_id': envio_id,
            'message': f'Te has unido al tracking del envío {envio_id}'
        })

        if estado_actual:  # Verificar que no sea None
            emit('status_update', estado_actual, room=f'envio_{envio_id}')
    else:
        print(f'❌ Permiso denegado para {user_type} {user_id} en envío {envio_id}')
        emit('error', {'message': 'No tienes permisos para trackear este envío'})

@socketio.on('leave_tracking')
def handle_leave_tracking(data):
    """Cliente deja de trackear un envío"""
    envio_id = data.get('envio_id')
    leave_room(f'envio_{envio_id}')
    emit('left_tracking', {'envio_id': envio_id})

@socketio.on('update_location')
def handle_location_update(data):
    """Conductor actualiza su ubicación"""
    conductor_id = data.get('conductor_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    timestamp = datetime.now()
    
    # Actualizar ubicación en base de datos
    actualizar_ubicacion_conductor(conductor_id, latitude, longitude, timestamp)
    
    # Obtener envíos activos del conductor
    envios_activos = get_envios_activos_by_conductor(conductor_id)
    
    # Emitir actualización a todos los clientes siguiendo estos envíos
    for envio in envios_activos:
        socketio.emit('location_update', {
            'envio_id': envio['id'],
            'conductor_id': conductor_id,
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': timestamp.isoformat()
        }, room=f'envio_{envio["id"]}')

def verificar_permiso_seguimiento(envio_id, user_id, user_type) -> bool:
    """Verificar si el usuario puede trackear el envío"""
    try:
        envio = Envio.query.get(envio_id)
        if not envio:
            return False

        if user_type == 'cliente':
            # Verificar tanto remitente como receptor
            return envio.remitente_id == user_id or envio.receptor_id == user_id
        elif user_type == 'conductor':
            return envio.conductor_id == user_id
        elif user_type == 'admin':  # Agregar soporte para admin
            return True
        return False
    except Exception as e:
        print(f"Error verificando permisos: {e}")
        return False

def get_envio_status(envio_id):
    """Obtener estado actual del envío"""
    try:
        envio = Envio.query.get(envio_id)
        if not envio:
            return None

        # Obtener datos relacionados
        conductor = Conductor.query.get(envio.conductor_id) if envio.conductor_id else None
        remitente = Cliente.query.get(envio.remitente_id) if envio.remitente_id else None
        receptor = Cliente.query.get(envio.receptor_id) if envio.receptor_id else None
        
        # Obtener última ubicación del conductor
        ubicacion = (Localizacion.query
                    .filter_by(conductor_id=envio.conductor_id)
                    .order_by(Localizacion.timestamp.desc())
                    .first()) if envio.conductor_id else None

        return {
            'envio_id': envio.id,
            'estado': envio.estado,
            'direccion_origen': envio.direccion_origen,
            'direccion_destino': envio.direccion_destino,
            'conductor_nombre': conductor.nombre if conductor else None,
            'conductor_id': envio.conductor_id,
            'remitente_nombre': remitente.nombre if remitente else None,
            'receptor_nombre': receptor.nombre if receptor else None,
            'latitude': ubicacion.latitude if ubicacion else None,
            'longitude': ubicacion.longitude if ubicacion else None,
            'last_location_update': ubicacion.timestamp.isoformat() if ubicacion else None
        }
    except Exception as e:
        print(f"Error obteniendo estado del envío {envio_id}: {e}")
        return None

def actualizar_ubicacion_conductor(conductor_id, latitude, longitude, timestamp):
    """Actualizar ubicación del conductor en la base de datos"""
    try:
        # Buscar ubicación existente
        ubicacion = Localizacion.query.filter_by(conductor_id=conductor_id).first()
        
        if not ubicacion:
            # Crear nueva ubicación
            ubicacion = Localizacion(
                conductor_id=conductor_id,
                latitude=latitude,
                longitude=longitude,
                timestamp=timestamp
            )
            db.session.add(ubicacion)
        else:
            # Actualizar ubicación existente
            ubicacion.latitude = latitude
            ubicacion.longitude = longitude
            ubicacion.timestamp = timestamp

        db.session.commit()
        print(f"✅ Ubicación actualizada para conductor {conductor_id}")
        
    except Exception as e:
        print(f"❌ Error actualizando ubicación: {e}")
        db.session.rollback()

def get_envios_activos_by_conductor(conductor_id):
    """Obtener envíos activos de un conductor"""
    try:
        # Estados que consideramos "activos"
        estados_activos = ["preparacion", "transito"]
        
        # Query simplificada para obtener envíos activos
        envios_activos = (db.session.query(Envio)
                         .filter(
                             Envio.conductor_id == conductor_id,
                             Envio.estado.in_(estados_activos)
                         )
                         .all())
        
        return [{'id': envio.id} for envio in envios_activos]
        
    except Exception as e:
        print(f"❌ Error obteniendo envíos activos: {e}")
        return []

def notificar_cambio_estado(envio_id):
    """Notificar cambio de estado a todos los clientes que trackean el envío"""
    try:
        estado_actualizado = get_envio_status(envio_id)
        if estado_actualizado:
            socketio.emit('status_update', estado_actualizado, room=f'envio_{envio_id}')
            print(f"✅ Notificación de cambio de estado enviada para envío {envio_id}")
    except Exception as e:
        print(f"❌ Error notificando cambio de estado: {e}")
