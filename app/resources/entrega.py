from flask_restful import Resource, reqparse
from app.services.entrega_service import crear_envio, actualizar_estado_envio, obtener_envios_por_usuario


# Gestiona nueva envio
class EnvioResource(Resource):
    def post(self):
        parser = reqparse.RequestParser() # asegura que recibo la info que necesito
        # espero recibir los siguientes campos
        parser.add_argument("remitente_id", type=str, required=True, help="remitente_id es requerido") #help indica lo que le envio de vuelta
        parser.add_argument("conductor_id", type=str, required=True, help="conductor_id es requerido")
        parser.add_argument("ruta_id", type=int, required=True, help="ruta_id es requerida")

        args = parser.parse_args() # lee los datos de la solicitud, crea un diccionario con los datos
        try:
            envio=crear_envio(
                remitente_id=args['remitente_id'], 
                ruta_id=args['ruta_id'], 
                conductor_id=args['conductor_id']
            )
            return {
                "mensaje": "Envío creado exitosamente",
                "envío": {
                    "id": envio.id,
                    "usuario id": envio.remitente_id,
                    "conductor id": envio.conductor_id,
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

