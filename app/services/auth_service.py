# ESTE ES SOLO UN EJEMPLO

import requests

def login_usuario(email, password):
    response = requests.post('http://servicio-auth:5000/login', json={
        'email': email,
        'password': password
    })
    return response.json(), response.status_code
