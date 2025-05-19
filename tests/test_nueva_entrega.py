import requests

BASE = "http://127.0.0.1:5000/"

nueva_entrega = {
    "usuario_id" : 2,
    "ruta_id" : 5,
    "peso" : 55,
    "dimensiones" : "10x10x10",
}

response = requests.post(BASE + "api/entregas", json=nueva_entrega)

print("Status code:", response.status_code)

try:
    print(response.json())
except Exception as e:
    print("Error al leer JSON de respuesta:", str(e))
    print("Texto recibido:", response.text)
