from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room
from app import socketio
from datetime import datetime
from app import db
from app.models import *

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
        print(f'📤 Enviando estado actual: {estado_actual}')  # Asegúrate de que no sea None

        emit('joined_tracking', {
            'envio_id': envio_id,
            'message': f'Te has unido al tracking del envío {envio_id}'
        })

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

# Consultas a la base de datos a través de nuestros modelos
def verificar_permiso_seguimiento(envio_id, user_id, user_type) -> bool:
    """Verificar si el usuario puede trackear el envío"""
    envio = Envio.query.get(envio_id)
    if not envio:
        return False

    if user_type == 'cliente':
        return envio.remitente_id == user_id
    elif user_type == 'conductor':
        return envio.conductor_id == user_id
    return False

def get_envio_status(envio_id):
    """Obtener estado actual del envío"""
    envio = Envio.query.get(envio_id)
    if not envio:
        return None

    conductor = Conductor.query.get(envio.conductor_id)
    cliente = Cliente.query.get(envio.remitente_id)
    ubicacion = Localizacion.query.filter_by(conductor_id=envio.conductor_id).order_by(Localizacion.timestamp.desc()).first()
    
    ultimo_estado = (
        sorted(envio.historial_estados, key=lambda e: e.timestamp, reverse=True)[0]
        if envio.historial_estados else None
    )

    return {
        'envio_id': envio.id,
        'estado': ultimo_estado.estado.estado.value if ultimo_estado else None,
        'direccion_origen': getattr(envio, 'direccion_origen', None),  # Solo si tienes estos campos en el modelo
        'direccion_destino': getattr(envio, 'direccion_destino', None),
        'conductor_nombre': conductor.nombre if conductor else None,
        'cliente_nombre': cliente.nombre if cliente else None,
        'latitude': ubicacion.latitude if ubicacion else None,
        'longitude': ubicacion.longitude if ubicacion else None,
        'last_location_update': ubicacion.updated_at.isoformat() if ubicacion else None
    }

def actualizar_ubicacion_conductor(conductor_id, latitude, longitude, timestamp):
    """Actualizar ubicación del conductor en la base de datos"""
    ubicacion = Localizacion.query.filter_by(conductor_id=conductor_id).first()
    if not ubicacion:
        ubicacion = Localizacion(
            conductor_id=conductor_id,
            latitude=latitude,
            longitude=longitude,
            timestamp=timestamp
        )
        db.session.add(ubicacion)
    else:
        ubicacion.latitude = latitude
        ubicacion.longitude = longitude
        ubicacion.timestamp = timestamp

    db.session.commit()

def get_envios_activos_by_conductor(conductor_id):
    """Obtener envíos activos de un conductor"""
    envios = Envio.query.filter(
        Envio.conductor_id == conductor_id,
        Envio.historial_estados.in_(['En preparación', 'En transito', 'Entregado'])
    ).all()

    return [{'id': envio.id} for envio in envios]

