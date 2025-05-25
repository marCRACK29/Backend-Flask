import requests

BASE = "http://127.0.0.1:5000/"

# ID del envío a modificar
envio_id = 7

# Cambiar el estado a "En tránsito"
payload = {
    "nuevo_estado": "En transito"  # Usando el valor directamente
}

# Realizar la petición
response = requests.put(f"{BASE}/api/envios/{envio_id}/estado", json=payload)

# Mostrar resultados
print("Status code:", response.status_code)
print("Respuesta:", response.json())