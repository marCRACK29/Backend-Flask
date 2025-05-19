import requests

BASE = "http://127.0.0.1:5000"
usuario_id=3

response = requests.get(f"{BASE}/api/entregas/mis", params={"usuario_id":usuario_id})

print("Status Code:", response.status_code)
print("Respuesta JSON:", response.json())