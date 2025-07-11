import requests
import os
from dotenv import load_dotenv
load_dotenv()
BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:5000/")

# ID del envío a modificar
envio_id = 4

# Cambiar el estado a "transito"
# Solo ocupar "transito" o "entregado" 
payload = {
    "nuevo_estado": "transito"  # Usando el valor del string directamente
}

# Realizar la petición
response = requests.put(f"{BASE}/api/envios/{envio_id}/estado", json=payload)

# Mostrar resultados
print("Status code:", response.status_code)
print("Respuesta:", response.json())