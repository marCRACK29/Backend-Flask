import requests
import os
from dotenv import load_dotenv
load_dotenv()
BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:5000/")

nuevo_envio = {
    "remitente_id": "21.595.999-3",
    "receptor_id" : "21.595.999-4",
    "paquetes": [
        {
            "peso": 10,
            "descripcion": "Caja de libros"
        },
        {
            "peso": 3,
            "descripcion": "Accesorios"
        }
    ]
}


response = requests.post(BASE + "api/envios", json=nuevo_envio)

print("Status code:", response.status_code)

try:
    print(response.json())
except Exception as e:
    print("Error al leer JSON de respuesta:", str(e))
    print("Texto recibido:", response.text)
