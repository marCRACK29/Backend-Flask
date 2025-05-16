import requests

BASE = "http://127.0.0.1:5000/"

nuevo_usuario = {
    "RUT": "12.345.678-9",
    "nombre": "Juan Pérez",
    "correo": "juan@example.com",
    "contraseña": "secreta123"
}

response = requests.post(BASE + "api/auth/register", json=nuevo_usuario)

print("Status code:", response.status_code)
print("Respuesta:", response.json())
