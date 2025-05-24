import requests

BASE = "http://127.0.0.1:5000/"

# Datos de prueba
conductor_id = "15.123.123-5"
envio_id = 5  # Asegúrate de que este envío exista y pertenezca al conductor
nuevo_estado = "Entregado"

# Realizar la petición PUT para actualizar el estado
response = requests.put(
    f"{BASE}api/conductor/envios/{envio_id}/estado",
    json={
        "conductor_id": conductor_id,
        "nuevo_estado": nuevo_estado
    }
)

print("Status code:", response.status_code)
try:
    print("Respuesta:", response.json())
except Exception as e:
    print("Error al leer JSON de respuesta:", str(e))
    print("Texto recibido:", response.text)

# Verificar el estado actual del envío
response_verificacion = requests.get(f"{BASE}api/conductor/envios/en-curso?conductor_id={conductor_id}")

print("\nVerificación del estado actual:")
print("Status code:", response_verificacion.status_code)
try:
    print("Respuesta:", response_verificacion.json())
except Exception as e:
    print("Error al leer JSON de respuesta:", str(e))
    print("Texto recibido:", response_verificacion.text) 