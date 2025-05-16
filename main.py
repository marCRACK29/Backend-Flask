#REST: REpresentation State Transfer
#API: Application Program Interface
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app) # Envolver la app en una API 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Como una tabla de base de datos
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False) # nullable=False indica que el campo es obligatorio
    likes = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(nombre={nombre}, likes={likes}, views={views})"

# Valida que al hacer put se envien todos los campos requeridos
video_put_args = reqparse.RequestParser() # Objeto analizador de solicitudes 
video_put_args.add_argument("nombre", type=str, help="Nombre del video", required=True) # required=True indica que el argumento es obligatorio
video_put_args.add_argument("likes", type=int, help="Likes del video", required=True)
video_put_args.add_argument("views", type=int, help="Vistas del video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("nombre", type=str, help="Nombre del video")
video_update_args.add_argument("likes", type=int, help="Likes del video")
video_update_args.add_argument("views", type=int, help="Vistas del video")

# Para que flask sepa cómo serializar un objeto videoModel a JSON
resource_fields = {
    'id': fields.Integer,
    'nombre': fields.String,
    'likes': fields.Integer,
    'views': fields.Integer
}

class Video(Resource):
    # Obtener un video
    @marshal_with(resource_fields) # Convierte el objeto VideoModel en un diccionario
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video no encontrado")
        return result
    
    # Crear un nuevo video
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video ya existe ...")
        video = VideoModel(id=video_id, nombre=args['nombre'], likes=args['likes'], views=args['views'])
        db.session.add(video)
        db.session.commit()
        return video, 201
    
    # Modificar un video existente
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        
        if not result:
            abort(404, message="Video no encontrado")
        if args['nombre']:
            result.nombre = args['nombre']
        if args['likes']:
            result.likes = args['likes']
        if args['views']:
            result.views = args['views']
        
        db.session.commit()
        return result
    
    # Eliminar un video
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video no encontrado")
        db.session.delete(result)
        db.session.commit()
        return '', 204

# Añadimos el recurso a la API
api.add_resource(Video, '/video/<int:video_id>') # <tipodato:nombre_variable>

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

