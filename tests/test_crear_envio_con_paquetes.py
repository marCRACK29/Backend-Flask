import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno (como API_BASE_URL)
load_dotenv()
BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:5000/")

nuevo_envio = {
    "remitente_id": "15.123.123-4",
    "ruta_id": 5,
    "conductor_id": "15.123.123-5",
    "paquetes": [
        {
            "peso": 5,
            "alto": 10,
            "largo": 20,
            "ancho": 15,
            "descripcion": "Zapatos deportivos"
        },
        {
            "peso": 3,
            "alto": 8,
            "largo": 18,
            "ancho": 10,
            "descripcion": "Artículos escolares"
        }
    ]
}

response = requests.post(BASE + "api/envios", json=nuevo_envio)

print("Status code:", response.status_code)

try:
    print("Respuesta JSON:")
    print(response.json())
except Exception as e:
    print("Error al leer JSON de respuesta:", str(e))
    print("Texto recibido:", response.text)
