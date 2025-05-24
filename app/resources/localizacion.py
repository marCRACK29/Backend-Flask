from flask_restful import Resource, reqparse
from app.services.localizacion_service import registrar_localizacion, obtener_ultima_localizacion, obtener_historial_localizaciones

class LocalizacionResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("envio_id", type=int, required=True)
        parser.add_argument("latitud", type=float, required=True)
        parser.add_argument("longitud", type=float, required=True)
        args = parser.parse_args()
        localizacion = registrar_localizacion(args["envio_id"], args["latitud"], args["longitud"])
        return {
            "id": localizacion.id,
            "envio_id": localizacion.envio_id,
            "latitud": localizacion.latitud,
            "longitud": localizacion.longitud,
            "timestamp": localizacion.timestamp.isoformat()
        }, 201

class UltimaLocalizacionResource(Resource):
    def get(self, envio_id):
        localizacion = obtener_ultima_localizacion(envio_id)
        if not localizacion:
            return {"mensaje": "No hay localización registrada para este envío"}, 404
        return {
            "latitud": localizacion.latitud,
            "longitud": localizacion.longitud,
            "timestamp": localizacion.timestamp.isoformat()
        }

class HistorialLocalizacionResource(Resource):
    def get(self, envio_id):
        historial = obtener_historial_localizaciones(envio_id)
        return [
            {
                "latitud": loc.latitud,
                "longitud": loc.longitud,
                "timestamp": loc.timestamp.isoformat()
            }
            for loc in historial
        ]