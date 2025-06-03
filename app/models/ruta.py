from app import db

class Ruta(db.Model):
    __tablename__ = 'ruta'

    id = db.Column(db.Integer, primary_key=True)
    distancia = db.Column(db.Float, nullable=False)
    duracion = db.Column(db.Float, nullable=False)