from app import db

class Paquete(db.Model):
    __tablename__ = 'paquete'

    id = db.Column(db.Integer, primary_key=True)
    peso = db.Column(db.Integer, nullable=False)
    alto = db.Column(db.Integer)
    largo = db.Column(db.Integer)
    ancho = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    envio_id = db.Column(db.Integer, db.ForeignKey('envio.id'), nullable=False)
    
    envio = db.relationship('Envio', back_populates='paquetes', foreign_keys=[envio_id])