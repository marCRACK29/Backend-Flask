import requests

BASE = "http://127.0.0.1:5000/"

nuevo_usuario = {
    "RUT": "21.123.123-4",
    "nombre": "Sebastián Vega",
    "correo": "seba@example.com",
    "contraseña": "holaaa"
}

response = requests.post(BASE + "api/auth/register", json=nuevo_usuario)

print("Status code:", response.status_code)
print("Respuesta:", response.json())
