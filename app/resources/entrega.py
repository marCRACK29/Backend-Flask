from flask_restful import Resource, reqparse
from app.services.entrega_service import crear_entrega, actualizar_estado_entrega, obtener_entregas_por_usuario

# Gestiona nueva entrega
class EntregaResource(Resource):
    def post(self):
        parser = reqparse.RequestParser() # asegura que recibo la info que necesito
        # espero recibir los siguientes campos
        parser.add_argument("usuario_id", type=int, required=True, help="usuario_id es requerido") #help indica lo que le envio de vuelta
        parser.add_argument("peso", type=int, required=True, help="peso es requerido")           #si no recibo lo que necesitaba
        parser.add_argument("dimensiones", type=str, required=True, help="dimensiones son requeridas")
        parser.add_argument("ruta_id", type=int, required=True, help="ruta_id es requerida")

        args = parser.parse_args() # lee los datos de la solicitud, crea un diccionario con los datos
        try:
            entrega=crear_entrega(
                usuario_id=args['usuario_id'], 
                ruta_id=args['ruta_id'], 
                peso=args['peso'], 
                dimensiones=args['dimensiones']
            )
            return {
                "mensaje": "Entrega creada exitosamente",
                "entrega": {
                    "id": entrega.id,
                    "usuario id": entrega.usuario_id,
                    "peso": float(entrega.peso), # Se debe especificar float ya que peso es Decimal pero Json no es serializable
                    "dimensiones": entrega.dimensiones,
                }
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400


# Gestiona cambio estado entrega
class EntregaEstadoResource(Resource):
    def put(self, entrega_id):
        parser = reqparse.RequestParser()
        parser.add_argument("nuevo_estado", type=int, required=True, help="nuevo_estado es requerido")
        args = parser.parse_args()

        try:
            nuevo_estado=actualizar_estado_entrega(entrega_id, args["nuevo_estado"])
            return{
                "mensaje": "Estado actualizado correctamente",
                "entrega_id": entrega_id,
                "nuevo_estado": nuevo_estado
                }, 200
        except ValueError as ve:
            return{"error":str(ve)},400
        except LookupError as le:
            return{"error":str(le)},404
        except Exception as e:
            return{"error": f"Error inesperado {str(e)}"}, 500
        
class EntregasClienteResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("usuario_id",type=int,required=True,location="args") #location args es que este dato viene de la url, no del body
        args = parser.parse_args()                                               #reqparse no los encuentra por defecto en el GET

        try:
            usuario_id = args["usuario_id"]
            entregas = obtener_entregas_por_usuario(usuario_id)

            if entregas is None:
                return{"mensaje": "Aun no has realizado entregas"}, 200
            return [
                {
                    "id": entrega.id,
                    "estado_id": entrega.estado_id,
                    "peso": float(entrega.peso),
                    "dimensiones": entrega.dimensiones,
                    "fecha_envio": entrega.fecha_envio.isoformat()
                }
                for entrega in entregas
            ], 200
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except RuntimeError as re:
            return {"error": str(re)}, 500
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500

