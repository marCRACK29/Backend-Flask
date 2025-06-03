import requests
import os
from dotenv import load_dotenv
load_dotenv()
BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:5000/")

# Datos de prueba con IDs que existen en la base de datos
nuevo_envio = {
    "remitente_id": "21.595.452-3",  # ID de un cliente que existe                  # ID de una ruta que existe
    "conductor_id": "15.123.102-4",  # ID de un conductor que existe
    "direccion_origen": "Los Ángeles",
    "direccion_destino": "Concepción"
}

print("Enviando datos:", nuevo_envio)
response = requests.post(BASE + "api/envios", json=nuevo_envio)
print("Status code:", response.status_code)

try:
    print(response.json())
except Exception as e:
    print("Error al leer JSON de respuesta:", str(e))
    print("Texto recibido:", response.text)
