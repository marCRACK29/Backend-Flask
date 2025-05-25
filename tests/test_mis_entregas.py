import requests
import os
from dotenv import load_dotenv
load_dotenv()
BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:5000/")

usuario_id="21.123.123-4"

response = requests.get(f"{BASE}/api/envios/mis", params={"usuario_id":usuario_id})

print("Status Code:", response.status_code)
print("Respuesta JSON:", response.json())