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
parser.add_argument('tipo_usuario', type=str, required=True, help="El tipo de usuario es obligatorio")
# Campos extra para cliente
parser.add_argument('numero_domicilio', type=int)
parser.add_argument('calle', type=str)
parser.add_argument('ciudad', type=str)
parser.add_argument('region', type=str)
parser.add_argument('codigo_postal', type=int)

# Clase encargada de registrar usuarios
class AuthRegisterResource(Resource):
    def post(self):
        args = parser.parse_args()

        try:
            usuario = registrar_usuario(
                RUT=args['RUT'],
                nombre=args['nombre'],
                correo=args['correo'],
                contraseña=args['contraseña'],
                tipo_usuario=args['tipo_usuario'],
                numero_domicilio=args.get('numero_domicilio'),
                calle=args.get('calle'),
                ciudad=args.get('ciudad'),
                region=args.get('region'),
                codigo_postal=args.get('codigo_postal')
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
