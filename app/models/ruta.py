from app import db

class Ruta(db.Model):
    __tablename__ = 'ruta'

    id = db.Column(db.Integer, primary_key=True)
    distancia = db.Column(db.Float, nullable=False)
    duracion = db.Column(db.Float, nullable=False)

    # Relación con envío
    ruta_envio = db.relationship('Envio', backref='ruta_en_envio', lazy=True)