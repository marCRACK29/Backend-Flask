import socketio
import time
import os
from dotenv import load_dotenv
load_dotenv()

# Configuración
BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")
sio = socketio.Client()

# Datos de prueba
conductor_id = "15.123.102-4"  # ID del conductor que existe
latitude = -36.838709 
longitude = -73.095146

# Variable para verificar si recibimos la actualización
actualizacion_recibida = False

@sio.event
def connect():
    print("✅ Conectado al servidor")

@sio.event
def connect_error(data):
    print("❌ Error de conexión:", data)

@sio.event
def disconnected():
    print("❌ Desconectado del servidor")

@sio.on('location_update')
def on_location_update(data):
    global actualizacion_recibida
    print("\n📡 Actualización de ubicación recibida:")
    print(f"Conductor ID: {data['conductor_id']}")
    print(f"Latitud: {data['latitude']}")
    print(f"Longitud: {data['longitude']}")
    print(f"Timestamp: {data['timestamp']}")
    actualizacion_recibida = True

def test_actualizar_localizacion():
    try:
        # Conectar al servidor
        sio.connect(BASE_URL)
        print("🔄 Enviando actualización de ubicación...")
        
        # Unirse al tracking de un envío
        sio.emit('join_tracking', {
            'envio_id': 1,  # ID de un envío existente
            'user_type': 'admin',
            'user_id': 'admin1'
        })
        
        # Enviar actualización de ubicación
        sio.emit('update_location', {
            'conductor_id': conductor_id,
            'latitude': latitude,
            'longitude': longitude
        })
        
        # Esperar un momento para que el servidor procese la actualización
        time.sleep(2)
        
        if actualizacion_recibida:
            print("\n✅ Test completado exitosamente:")
            print("- Se envió la actualización de ubicación")
            print("- Se recibió la confirmación del servidor")
            print("- El front debería haber recibido la actualización")
        else:
            print("\n❌ No se recibió la actualización de ubicación")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        sio.disconnect()

if __name__ == "__main__":
    test_actualizar_localizacion() 