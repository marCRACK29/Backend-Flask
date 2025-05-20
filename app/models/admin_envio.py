from app import db

class AdminEnvio(db.Model):
    __tablename__ = 'gestiona_envio'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(12), db.ForeignKey('admin.RUT'), nullable=False)
    envio_id = db.Column(db.Integer, db.ForeignKey('envio.id_envio'), nullable=False)

    admin = db.relationship('Admin', back_populates='envios_gestionados')
    envio = db.relationship('Envio', back_populates='gestiones_admin')