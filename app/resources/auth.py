# ESTE ES SOLO UN EJEMPLO. 

from flask_restful import Resource, reqparse
from app.services.auth_service import login_usuario, registrar_usuario

class AuthResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        return login_usuario(args['email'], args['password'])

# Para registrar usuarios
parser = reqparse.RequestParser()
parser.add_argument('RUT', type=str, required=True, help="El RUT es obligatorio")
parser.add_argument('nombre', type=str, required=True, help="El nombre es obligatorio")
parser.add_argument('correo', type=str, required=True, help="El correo es obligatorio")
parser.add_argument('contraseña', type=str, required=True, help="La contraseña es obligatoria")

# Clase encargada de registrar usuarios
class AuthRegisterResource(Resource):
    def post(self):
        args = parser.parse_args()

        try:
            usuario = registrar_usuario(
                RUT=args['RUT'],
                nombre=args['nombre'],
                correo=args['correo'],
                contraseña=args['contraseña']
            )
            return {
                "mensaje": "Usuario registrado exitosamente",
                "usuario": {
                    "RUT": usuario.RUT,
                    "nombre": usuario.nombre,
                    "correo": usuario.correo
                }
            }, 201

        except ValueError as e:
            return {"error": str(e)}, 400
