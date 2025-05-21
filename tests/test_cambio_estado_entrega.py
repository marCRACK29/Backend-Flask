import requests

BASE = "http://127.0.0.1:5000/"

envio_id = 1

payload = {
    "nuevo_estado":2
}

response = requests.put(f"{BASE}/api/envios/{envio_id}/estado", json=payload)

print("Status code:", response.status_code)
print(response.json())