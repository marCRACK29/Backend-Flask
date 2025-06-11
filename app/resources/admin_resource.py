from flask_restful import Resource, reqparse
from app.services.envio_service import asignar_conductor_a_envio
from app.models.conductor import Conductor
from app.models.envio import Envio 

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

class ListaConductoresResource(Resource):
    def get(self):
        conductores = Conductor.query.all()
        return {
            "conductores": [
                {
                    "RUT": c.RUT,
                    "nombre": c.nombre,      # Ajusta los campos según tu modelo
                } for c in conductores
            ]
        }, 200

class EnviosSinConductorResource(Resource):
    def get(self):
        envios = Envio.query.filter_by(conductor_id=None).all()
        return {
            "envios": [
                {
                    "id": e.id,
                    "direccion_destino": e.direccion_destino,   # Ajusta según los campos que quieras mostrar
                    "estado": e.estado.to_dict()
                } for e in envios
            ]
        }, 200
