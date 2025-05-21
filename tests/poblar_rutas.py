import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# Lista de rutas de ejemplo
rutas = [
    {
        "distancia": 5.2,  # en kilómetros
        "duracion": 15.0   # en minutos
    },
    {
        "distancia": 8.7,
        "duracion": 25.0
    },
    {
        "distancia": 12.3,
        "duracion": 35.0
    },
    {
        "distancia": 3.5,
        "duracion": 10.0
    },
    {
        "distancia": 7.8,
        "duracion": 22.0
    }
]

def crear_rutas():
    print("Creando rutas de prueba...")
    for ruta in rutas:
        response = requests.post(f"{BASE_URL}/api/rutas", json=ruta)
        if response.status_code == 201:
            print(f"Ruta creada exitosamente: {ruta}")
        else:
            print(f"Error al crear ruta: {ruta}")
            print(f"Error: {response.json()}")

if __name__ == "__main__":
    crear_rutas() 