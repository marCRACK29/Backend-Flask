from flask_restful import Resource, reqparse
from app.services.auth_service import login_usuario, registrar_cliente, registrar_conductor, registrar_admin

class AuthResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        return login_usuario(args['email'], args['password'])

class AuthRegisterClienteResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        
        # Campos básicos obligatorios
        parser.add_argument('RUT', type=str, required=True, help="El RUT es obligatorio")
        parser.add_argument('nombre', type=str, required=True, help="El nombre es obligatorio")
        parser.add_argument('correo', type=str, required=True, help="El correo es obligatorio")
        parser.add_argument('contraseña', type=str, required=True, help="La contraseña es obligatoria")
        
        # Campos de dirección obligatorios para clientes
        parser.add_argument('numero_domicilio', type=int, required=True, help="El número de domicilio es obligatorio")
        parser.add_argument('calle', type=str, required=True, help="La calle es obligatoria")
        parser.add_argument('ciudad', type=str, required=True, help="La ciudad es obligatoria")
        parser.add_argument('region', type=str, required=True, help="La región es obligatoria")
        parser.add_argument('codigo_postal', type=int, required=True, help="El código postal es obligatorio")
        
        args = parser.parse_args()

        try:
            usuario = registrar_cliente(
                RUT=args['RUT'],
                nombre=args['nombre'],
                correo=args['correo'],
                contraseña=args['contraseña'],
                numero_domicilio=args['numero_domicilio'],
                calle=args['calle'],
                ciudad=args['ciudad'],
                region=args['region'],
                codigo_postal=args['codigo_postal']
            )
            
            return {
                "mensaje": "Cliente registrado exitosamente",
                "usuario": {
                    "RUT": usuario.RUT,
                    "nombre": usuario.nombre,
                    "correo": usuario.correo,
                    "direccion": {
                        "numero_domicilio": usuario.numero_domicilio,
                        "calle": usuario.calle,
                        "ciudad": usuario.ciudad,
                        "region": usuario.region,
                        "codigo_postal": usuario.codigo_postal
                    }
                }
            }, 201

        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"Error interno del servidor: {str(e)}"}, 500

class AuthRegisterConductorResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        
        # Campos básicos obligatorios
        parser.add_argument('RUT', type=str, required=True, help="El RUT es obligatorio")
        parser.add_argument('nombre', type=str, required=True, help="El nombre es obligatorio")
        parser.add_argument('correo', type=str, required=True, help="El correo es obligatorio")
        parser.add_argument('contraseña', type=str, required=True, help="La contraseña es obligatoria")
        
        args = parser.parse_args()

        try:
            usuario = registrar_conductor(
                RUT=args['RUT'],
                nombre=args['nombre'],
                correo=args['correo'],
                contraseña=args['contraseña']
            )
            
            return {
                "mensaje": "Conductor registrado exitosamente",
                "usuario": {
                    "RUT": usuario.RUT,
                    "nombre": usuario.nombre,
                    "correo": usuario.correo
                }
            }, 201

        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"Error interno del servidor: {str(e)}"}, 500

class AuthRegisterAdminResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        
        # Campos básicos obligatorios
        parser.add_argument('RUT', type=str, required=True, help="El RUT es obligatorio")
        parser.add_argument('nombre', type=str, required=True, help="El nombre es obligatorio")
        parser.add_argument('correo', type=str, required=True, help="El correo es obligatorio")
        parser.add_argument('contraseña', type=str, required=True, help="La contraseña es obligatoria")
        
        args = parser.parse_args()

        try:
            usuario = registrar_admin(
                RUT=args['RUT'],
                nombre=args['nombre'],
                correo=args['correo'],
                contraseña=args['contraseña']
            )
            
            return {
                "mensaje": "Admin registrado exitosamente",
                "usuario": {
                    "RUT": usuario.RUT,
                    "nombre": usuario.nombre,
                    "correo": usuario.correo
                }
            }, 201

        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"Error interno del servidor: {str(e)}"}, 500