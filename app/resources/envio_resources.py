from flask_restful import Resource, reqparse
from app.services.envio_service import crear_envio, actualizar_estado_envio, obtener_envios_por_usuario, obtener_envios_por_conductor
from app.models.envio import Envio
import enum


# Gestiona nueva envio
class EnvioResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("remitente_id", type=str, required=True, help="remitente_id es requerido")
        parser.add_argument("conductor_id", type=str, required=True, help="conductor_id es requerido")
        parser.add_argument("ruta_id", type=int, required=True, help="ruta_id es requerida")
        parser.add_argument("direccion_origen", type=str, required=True, help="direccion_origen es requerida")
        parser.add_argument("direccion_destino", type=str, required=True, help="direccion_destino es requerida")
        parser.add_argument("receptor_id", type=str, required=False, help="receptor_id es opcional")

        args = parser.parse_args()
        try:
            envio = crear_envio(
                remitente_id=args['remitente_id'], 
                ruta_id=args['ruta_id'], 
                conductor_id=args['conductor_id'],
                direccion_origen=args['direccion_origen'],
                direccion_destino=args['direccion_destino'],
                receptor_id=args.get('receptor_id')
            )
            return {
                "mensaje": "Envío creado exitosamente",
                "envío": {
                    "id": envio.id,
                    "remitente_id": envio.remitente_id,
                    "receptor_id": envio.receptor_id,
                    "conductor_id": envio.conductor_id,
                    "ruta_id": envio.ruta_id,
                    "direccion_origen": envio.direccion_origen,
                    "direccion_destino": envio.direccion_destino
                }
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400
        

    # def get(self, envio_id=None):
    #     """Obtener un envío específico por ID"""
    #     if envio_id is None:
    #         return {'error': 'ID de envío requerido'}, 400
            
    #     try:
    #         envio = Envio.query.get(envio_id)
            
    #         if not envio:
    #             return {'error': 'Envío no encontrado'}, 404
            
    #         # Obtener el último estado del historial
    #         ultimo_estado = envio.historial_estados[-1] if envio.historial_estados else None
            
    #         # Serializar el envío a JSON
    #         envio_data = {
    #             'id': envio.id,
    #             'remitente_id': envio.remitente_id,
    #             'receptor_id': envio.receptor_id,
    #             'conductor_id': envio.conductor_id,
    #             'ruta_id': envio.ruta_id,
    #             'direccion_origen': envio.direccion_origen,
    #             'direccion_destino': envio.direccion_destino,
    #             'created_at': envio.created_at.isoformat() if envio.created_at else None,
    #             'updated_at': envio.updated_at.isoformat() if envio.updated_at else None,
    #             'estado_actual': {
    #                 'estado': ultimo_estado.estado.estado.value if ultimo_estado else 'Sin estado',
    #                 'timestamp': ultimo_estado.timestamp.isoformat() if ultimo_estado else None,
    #                 'detalles': ultimo_estado.detalles if ultimo_estado else None
    #             }
    #         }
            
    #         return envio_data, 200
            
    #     except Exception as e:
    #         return {'error': f'Error interno del servidor: {str(e)}'}, 500

    # def get_estado(self, envio_id):
    #     """Obtener el estado actual de un envío específico"""
    #     try:
    #         envio = Envio.query.get(envio_id)
            
    #         if not envio:
    #             return {'error': 'Envío no encontrado'}, 404
            
    #         # Obtener el último estado del historial
    #         ultimo_estado = envio.historial_estados[-1] if envio.historial_estados else None
            
    #         if not ultimo_estado:
    #             return {
    #                 'envio_id': envio.id,
    #                 'estado': 'Sin estado registrado',
    #                 'timestamp': None
    #             }, 200
            
    #         return {
    #             'envio_id': envio.id,
    #             'estado': ultimo_estado.estado.estado.value,
    #             'timestamp': ultimo_estado.timestamp.isoformat(),
    #             'detalles': ultimo_estado.detalles
    #         }, 200
            
    #     except Exception as e:
    #         return {'error': f'Error interno del servidor: {str(e)}'}, 500



# Gestiona cambio estado envio
class EnvioEstadoResource(Resource):
    def put(self, envio_id):
        parser = reqparse.RequestParser()
        parser.add_argument("nuevo_estado", type=str, required=True, help="nuevo_estado es requerido")
        args = parser.parse_args()

        try:
            nuevo_estado = actualizar_estado_envio(envio_id, args["nuevo_estado"])
            return {
                "mensaje": "Estado actualizado correctamente",
                "envio_id": envio_id,
                "nuevo_estado": nuevo_estado
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
        parser.add_argument("usuario_id",type=str,required=True,location="args") #location args es que este dato viene de la url, no del body
        args = parser.parse_args()                                               #reqparse no los encuentra por defecto en el GET

        try:
            usuario_id = args["usuario_id"]
            envios = obtener_envios_por_usuario(usuario_id)

            if envios is None:
                return{"mensaje": "Aun no has realizado envios"}, 200
            return [
                {
                    "id_envio": envio.id,
                    "estado_actual": envio.historial_estados[-1].estado.estado.value if envio.historial_estados else "Sin estado",
                    "fecha_ultimo_estado": envio.historial_estados[-1].timestamp.isoformat() if envio.historial_estados else None
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
                    "estado_actual": envio.historial_estados[-1].estado.estado.value if envio.historial_estados else "Sin estado",
                    "fecha_ultimo_estado": envio.historial_estados[-1].timestamp.isoformat() if envio.historial_estados else None,
                    "remitente": envio.remitente_id,
                    "receptor": envio.receptor_id,
                    "ruta_id": envio.ruta_id
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
                     
            estado_info = {
                'estado': 'Sin estado',
                'timestamp': None
            }
                     
            if envio.historial_estados:
                try:
                    ultimo_estado = envio.historial_estados[-1]
                    if ultimo_estado and hasattr(ultimo_estado, 'estado') and ultimo_estado.estado:
                        estado_valor = ultimo_estado.estado.estado
                        
                        # Múltiples formas de extraer el valor del enum
                        if hasattr(estado_valor, 'value'):
                            estado_str = str(estado_valor.value)
                        elif isinstance(estado_valor, enum.Enum):
                            estado_str = str(estado_valor.value)
                        else:
                            estado_str = str(estado_valor)
                        
                        estado_info = {
                            'estado': estado_str,
                            'timestamp': ultimo_estado.timestamp.isoformat() if hasattr(ultimo_estado, 'timestamp') and ultimo_estado.timestamp else None
                        }
                except (IndexError, AttributeError) as e:
                    print(f"Error accediendo al estado: {e}")
                     
            # Asegurar que todos los campos sean del tipo correcto
            envio_data = {
                'id': int(envio.id) if envio.id else 0,
                'remitente_id': str(envio.remitente_id) if envio.remitente_id else '',
                'receptor_id': str(envio.receptor_id) if envio.receptor_id else None,
                'conductor_id': str(envio.conductor_id) if envio.conductor_id else '',
                'ruta_id': int(envio.ruta_id) if envio.ruta_id else None,
                'direccion_origen': str(envio.direccion_origen) if envio.direccion_origen else '',
                'direccion_destino': str(envio.direccion_destino) if envio.direccion_destino else '',
                'estado_actual': estado_info['estado']  # Solo guardamos el string del estado
            }
            
            # Debug: imprimir la respuesta para verificar tipos
            print(f"Enviando datos: {envio_data}")
            print(f"Tipo de estado: {type(estado_info['estado'])}")
                     
            return envio_data, 200
                 
        except Exception as e:
            print(f"Error en EnvioIndividualResource: {str(e)}")
            return {'error': f'Error interno del servidor: {str(e)}'}, 500