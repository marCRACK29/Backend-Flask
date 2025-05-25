import requests

BASE = "http://127.0.0.1:5000/"

# Datos de prueba
cliente_rut = "21.595.999-3"
nueva_direccion = {
    "calle": "calle verdadera",
    "numero_domicilio": 666,
    "ciudad": "conce",
    "region": "Metropolitana",
    "codigo_postal": 1234567
}
nuevo_correo = "rodolfo@ejemplo.com"

print("=== Test de Servicios de Cliente ===")

# 1. Actualizar dirección
print("\n1. Actualizando dirección del cliente...")
response_direccion = requests.put(
    f"{BASE}api/cliente/direccion",
    json={
        "rut_cliente": cliente_rut,
        **nueva_direccion
    }
)

print("Status code:", response_direccion.status_code)
try:
    print("Respuesta:", response_direccion.json())
except Exception as e:
    print("Error al leer JSON de respuesta:", str(e))
    print("Texto recibido:", response_direccion.text)

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