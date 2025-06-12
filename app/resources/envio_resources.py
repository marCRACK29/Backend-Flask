from flask_restful import Resource, reqparse
from app.services.envio_service import crear_envio, actualizar_estado_envio, obtener_envios_por_usuario, obtener_envios_por_conductor
from app.models.envio import Envio

# Gestiona nuevo envio
class EnvioResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("remitente_id", type=str, required=True, help="remitente_id es requerido")
        parser.add_argument("direccion_origen", type=str, required=True, help="direccion_origen es requerida")
        parser.add_argument("direccion_destino", type=str, required=True, help="direccion_destino es requerida")
        parser.add_argument("receptor_id", type=str, required=False, help="receptor_id es opcional")

        args = parser.parse_args()
        try:
            envio = crear_envio(args)
            return {
                "mensaje": "Envío creado exitosamente",
                "envío": {
                    "id": envio.id,
                    "remitente_id": envio.remitente_id,
                    "receptor_id": envio.receptor_id,
                    "direccion_origen": envio.direccion_origen,
                    "direccion_destino": envio.direccion_destino,
                    "estado": envio.estado.to_dict() if envio.estado else None
                }
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400

class EnvioEstadoResource(Resource):
    def put(self, envio_id):
        parser = reqparse.RequestParser()
        parser.add_argument("nuevo_estado", type=str, required=True, help="nuevo_estado es requerido")
        args = parser.parse_args()

        try:
            envio = actualizar_estado_envio(envio_id, args["nuevo_estado"])
            return {
                "mensaje": "Estado actualizado correctamente",
                "envio_id": envio_id,
                "nuevo_estado": envio.estado.to_dict() if envio.estado else None
            }, 200
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except LookupError as le:
            return {"error": str(le)}, 404
        except Exception as e:
            return {"error": f"Error inesperado {str(e)}"}, 500
        
class EnviosClienteResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("usuario_id",type=str,required=True,location="args")
        args = parser.parse_args()

        try:
            usuario_id = args["usuario_id"]
            envios = obtener_envios_por_usuario(usuario_id)

            if envios is None:
                return{"mensaje": "Aun no has realizado envios"}, 200
            return [
                {
                    "id_envio": envio.id,
                    "estado_actual": envio.estado.to_dict() if envio.estado else None,
                    "receptor_id": envio.receptor_id,
                    "direccion_destino": envio.direccion_destino
                }
                for envio in envios
            ], 200
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except RuntimeError as re:
            return {"error": str(re)}, 500
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500

class EnviosConductorResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("conductor_id", type=str, required=True, location="args")
        args = parser.parse_args()

        try:
            conductor_id = args["conductor_id"]
            envios = obtener_envios_por_conductor(conductor_id)

            if envios is None:
                return {"mensaje": "No tienes envíos asignados"}, 200
                
            return [
                {
                    "id_envio": envio.id,
                    "estado_actual": envio.estado.to_dict() if envio.estado else None,
                    "direccion_destino": str(envio.direccion_destino) if envio.direccion_destino else '',
                    "remitente": envio.remitente_id,
                    "receptor": envio.receptor_id,
                    "conductor_id": str(envio.conductor_id) if envio.conductor_id else ''
                }
                for envio in envios
            ], 200
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except RuntimeError as re:
            return {"error": str(re)}, 500
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500

class EnvioIndividualResource(Resource):
    def get(self, envio_id):
        """Obtener un envío específico por ID"""
        try:
            envio = Envio.query.get(envio_id)
                     
            if not envio:
                return {'error': 'Envío no encontrado'}, 404
                     
            envio_data = {
                'id': int(envio.id) if envio.id else 0,
                'remitente_id': str(envio.remitente_id) if envio.remitente_id else '',
                'receptor_id': str(envio.receptor_id) if envio.receptor_id else None,
                'conductor_id': str(envio.conductor_id) if envio.conductor_id else '',
                'direccion_origen': str(envio.direccion_origen) if envio.direccion_origen else '',
                'direccion_destino': str(envio.direccion_destino) if envio.direccion_destino else '',
                'estado_actual': envio.estado.to_dict() if envio.estado else None
            }
                     
            return envio_data, 200
                 
        except Exception as e:
            print(f"Error en EnvioIndividualResource: {str(e)}")
            return {'error': f'Error interno del servidor: {str(e)}'}, 500