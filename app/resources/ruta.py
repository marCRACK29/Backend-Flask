from flask_restful import Resource, reqparse
from app import db
from app.models import Ruta
from sqlalchemy.exc import IntegrityError

# Parser para validar los datos de entrada
ruta_parser = reqparse.RequestParser()
ruta_parser.add_argument('distancia', type=float, required=True, help="La distancia es obligatoria")
ruta_parser.add_argument('duracion', type=float, required=True, help="La duración es obligatoria")

class RutaResource(Resource):
    def post(self):
        """
        Crea una nueva ruta
        """
        args = ruta_parser.parse_args()
        
        try:
            nueva_ruta = Ruta(
                distancia=args['distancia'],
                duracion=args['duracion']
            )
            
            db.session.add(nueva_ruta)
            db.session.commit()
            
            return {
                "mensaje": "Ruta creada exitosamente",
                "ruta": {
                    "id": nueva_ruta.id,
                    "distancia": nueva_ruta.distancia,
                    "duracion": nueva_ruta.duracion
                }
            }, 201
            
        except IntegrityError:
            db.session.rollback()
            return {"error": "No se pudo crear la ruta"}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400 