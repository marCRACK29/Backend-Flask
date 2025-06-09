from flask_restful import Resource, reqparse
from app.services.auth_service import login_usuario, registrar_cliente, registrar_conductor, registrar_admin
from flask import request
from app.models import Cliente, Conductor, Admin
import jwt
from flask import current_app
from app import db
class AuthResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('correo', type=str, required=True, help="El correo es obligatorio")
        parser.add_argument('contraseña', type=str, required=True, help="La contraseña es obligatoria")
        args = parser.parse_args()

        try:
            return login_usuario(args['correo'], args['contraseña'])
        except Exception as e:
            print(f"Error en login: {str(e)}")  # Debug log
            return {'error': f'Error interno del servidor: {str(e)}'}, 500

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
        

class LogoutResource(Resource):
    def post(self):
        # En JWT no necesitas hacer logout del lado del servidor
        # Solo necesitas que el cliente elimine el token
        return {'message': 'Logout exitoso'}, 200

class ProfileResource(Resource):
    def get(self):
        try:
            # Obtener token del header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return {'error': 'Token no proporcionado'}, 401
            
            token = auth_header.split(' ')[1]
            
            # Decodificar token
            try:
                payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return {'error': 'Token expirado'}, 401
            except jwt.InvalidTokenError:
                return {'error': 'Token inválido'}, 401
            
            # Buscar usuario según el tipo
            user_id = payload['user_id']
            tipo = payload['tipo']
            
            usuario = None
            if tipo == 'cliente':
                usuario = Cliente.query.get(user_id)
            elif tipo == 'conductor':
                usuario = Conductor.query.get(user_id)
            elif tipo == 'admin':
                usuario = Admin.query.get(user_id)
            
            if not usuario:
                return {'error': 'Usuario no encontrado'}, 404
            
            user_data = {
                'id': usuario.RUT,
                'name': usuario.nombre,
                'email': usuario.correo,
                'tipo': tipo
            }
            
            # Agregar datos específicos del cliente si es necesario
            if tipo == 'cliente':
                user_data['direccion'] = {
                    'numero_domicilio': usuario.numero_domicilio,
                    'calle': usuario.calle,
                    'ciudad': usuario.ciudad,
                    'region': usuario.region,
                    'codigo_postal': usuario.codigo_postal
                }
            
            return user_data, 200
            
        except Exception as e:
            return {'error': 'Error interno del servidor'}, 500

    def put(self):
        try:
            # Obtener token del header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return {'error': 'Token no proporcionado'}, 401
            
            token = auth_header.split(' ')[1]
            
            # Decodificar token
            try:
                payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return {'error': 'Token expirado'}, 401
            except jwt.InvalidTokenError:
                return {'error': 'Token inválido'}, 401
            
            # Parser para obtener datos del request
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=False)
            parser.add_argument('phone', type=str, required=False)
            args = parser.parse_args()
            
            user_id = payload['user_id']
            tipo = payload['tipo']
            
            # Buscar usuario según el tipo
            usuario = None
            if tipo == 'cliente':
                usuario = Cliente.query.get(user_id)
            elif tipo == 'conductor':
                usuario = Conductor.query.get(user_id)
            elif tipo == 'admin':
                usuario = Admin.query.get(user_id)
            
            if not usuario:
                return {'error': 'Usuario no encontrado'}, 404
            
            # Actualizar campos
            if args['name']:
                usuario.nombre = args['name']
            
            # Commit cambios
            db.session.commit()
            
            user_data = {
                'id': usuario.RUT,
                'name': usuario.nombre,
                'email': usuario.correo,
                'tipo': tipo
            }
            
            # Agregar datos específicos del cliente si es necesario
            if tipo == 'cliente':
                user_data['direccion'] = {
                    'numero_domicilio': usuario.numero_domicilio,
                    'calle': usuario.calle,
                    'ciudad': usuario.ciudad,
                    'region': usuario.region,
                    'codigo_postal': usuario.codigo_postal
                }
            
            return user_data, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Error interno del servidor'}, 500        