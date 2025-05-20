from app import db

class Paquete(db.Model):
    __tablename__ = 'paquete'

    id_paquete = db.Column(db.Integer, primary_key=True)
    peso = db.Column(db.Integer, nullable=False)
    alto = db.Column(db.Integer)
    largo = db.Column(db.Integer)
    ancho = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    envio_id = db.Column(db.Integer, db.ForeignKey('envio.id_envio'), nullable=False)
    
    envio = db.relationship('Envio', foreign_keys=[envio_id])