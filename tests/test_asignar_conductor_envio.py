import requests
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()
BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:5000/")

# ID del envío que quieres actualizar
envio_id = 1

# RUT del conductor a asignar
rut_conductor = "15.123.123-5"

# Endpoint completo
url = f"{BASE}/api/envios/{envio_id}/asignar_conductor"

# Enviar solicitud PUT
response = requests.put(url, json={"rut_conductor": rut_conductor})

# Mostrar resultado
print("Status code:", response.status_code)
try:
    print("Respuesta JSON:", response.json())
except Exception:
    print("Respuesta texto:", response.text)
