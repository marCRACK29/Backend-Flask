# tests/test_crear_envio.py

import requests
import os
from dotenv import load_dotenv

# Cargar .env
load_dotenv()
BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")

# Datos del envío de prueba
nuevo_envio = {
    "remitente_id": "21.595.999-4",
    "receptor_id": "21.595.999-5",
    "direccion_destino": "Av. Siempre Viva 742, Springfield"
}

# Enviar petición POST
response = requests.post(BASE + "/api/envios", json=nuevo_envio)

# Imprimir resultado
print("Status code:", response.status_code)

try:
    print("Respuesta JSON:", response.json())
except Exception as e:
    print("Error al leer respuesta JSON:", e)
    print("Texto recibido:", response.text)
