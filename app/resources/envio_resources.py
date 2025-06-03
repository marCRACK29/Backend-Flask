from flask_restful import Resource, reqparse, request
from app.services.envio_service import actualizar_estado_envio, obtener_envios_por_usuario, obtener_envios_por_conductor,crear_envio, asignar_conductor_a_envio, asignar_ruta_a_envio


# Gestiona nueva envio
class EnvioResource(Resource):
    def post(self):
        parser = reqparse.RequestParser() # asegura que recibo la info que necesito
        # espero recibir los siguientes campos
        parser.add_argument("remitente_id", type=str, required=True, help="remitente_id es requerido") #help indica lo que le envio de vuelta
        parser.add_argument("receptor_id", type=str, required=True, help="receptor_id es requerido")
        parser.add_argument("direccion_destino", type=str, required=True, help="direccion_destino es requerido")

        args = parser.parse_args() # lee los datos de la solicitud, crea un diccionario con los datos
        try:
            if args['remitente_id']==args['receptor_id']:
                raise 
            envio=crear_envio(
                remitente_id=args['remitente_id'], 
                receptor_id=args['receptor_id'], 
                direccion_destino=args['direccion_destino']
            )
            return {
                "mensaje": "Envío creado exitosamente",
                "envío": {
                    "id": envio.id,
                    "remitente_id": envio.remitente_id,
                    "receptor_id": envio.receptor_id,
                    "direccion_destino": envio.direccion_destino,
                }
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400
        


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
        parser.add_argument("usuario_id", type=str, required=True, location="args")
        args = parser.parse_args()

        try:
            usuario_id = args["usuario_id"]
            envios = obtener_envios_por_usuario(usuario_id)

            if envios is None:
                return {"mensaje": "Aún no has realizado envíos"}, 200

            resultado = []

            for envio in envios:
                estado_actual = (
                    envio.historial_estados[-1].estado.estado.value
                    if envio.historial_estados else "Sin estado"
                )

                fecha_estado = (
                    envio.historial_estados[-1].timestamp.isoformat()
                    if envio.historial_estados else None
                )

                resultado.append({
                    "id_envio": envio.id,
                    "estado_actual": estado_actual,
                    "fecha_ultimo_estado": fecha_estado,
                    "receptor_id": envio.receptor_id,
                    "direccion_destino": envio.direccion_destino,
                })

            return resultado, 200

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


class AsignarConductorResource(Resource):
    def put(self, envio_id):
        parser = reqparse.RequestParser()
        parser.add_argument("rut_conductor", type=str, required=True, help="El RUT del conductor es obligatorio.")
        args = parser.parse_args()

        try:
            envio = asignar_conductor_a_envio(envio_id, args["rut_conductor"])
            return {"mensaje": "Conductor asignado exitosamente", "envio_id": envio.id, "conductor_id": envio.conductor_id}, 200
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500

class AsignarRutaResource(Resource):
    def put(self, envio_id):
        parser = reqparse.RequestParser()
        parser.add_argument("ruta_id", type=int, required=True, help="El ID de la ruta es obligatorio.")
        args = parser.parse_args()

        try:
            envio = asignar_ruta_a_envio(envio_id, args["ruta_id"])
            return {"mensaje": "Ruta asignada exitosamente", "envio_id": envio.id, "ruta_id": envio.ruta_id}, 200
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500