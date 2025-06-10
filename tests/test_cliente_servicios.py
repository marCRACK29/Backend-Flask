import requests
import os
from dotenv import load_dotenv
load_dotenv()
BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:5000/")

# Datos de prueba
cliente_rut = "21.595.452-3"

nuevo_correo = "rodolfo@ejemplo.com"

print("=== Test de Servicios de Cliente ===")

# 1. Obtener información del cliente
print("\n1. Obteniendo información del cliente...")
response_info = requests.get(
    f"{BASE}api/cliente/info",
    params={"rut_cliente": cliente_rut}
)

print("Status code:", response_info.status_code)
try:
    print("Respuesta:", response_info.json())
except Exception as e:
    print("Error al leer JSON de respuesta:", str(e))
    print("Texto recibido:", response_info.text)

# 2. Actualizar correo
print("\n2. Actualizando correo del cliente...")
response_correo = requests.put(
    f"{BASE}api/cliente/correo",
    json={
        "rut_cliente": cliente_rut,
        "nuevo_correo": nuevo_correo
    }
)

print("Status code:", response_correo.status_code)
try:
    print("Respuesta:", response_correo.json())
except Exception as e:
    print("Error al leer JSON de respuesta:", str(e))
    print("Texto recibido:", response_correo.text)

# 3. Obtener envíos del cliente
print("\n3. Obteniendo envíos del cliente...")
response_envios = requests.get(
    f"{BASE}api/cliente/envios",
    params={"rut_cliente": cliente_rut}
)

print("Status code:", response_envios.status_code)
try:
    print("Respuesta:", response_envios.json())
except Exception as e:
    print("Error al leer JSON de respuesta:", str(e))
    print("Texto recibido:", response_envios.text)

# 4. Probar con un RUT inexistente
print("\n4. Probando con un RUT inexistente...")
response_error = requests.get(
    f"{BASE}api/cliente/info",
    params={"rut_cliente": "99.999.999-9"}
)

print("Status code:", response_error.status_code)
try:
    print("Respuesta:", response_error.json())
except Exception as e:
    print("Error al leer JSON de respuesta:", str(e))
    print("Texto recibido:", response_error.text) 