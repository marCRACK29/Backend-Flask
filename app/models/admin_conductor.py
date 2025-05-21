from app import db

class AdminConductor(db.Model):
    __tablename__ = 'admin_conductor'

    id = db.Column(db.Integer, primary_key=True)
    id_conductor = db.Column(db.String(12), db.ForeignKey('conductor.RUT'), nullable=False)
    id_admin = db.Column(db.String(12), db.ForeignKey('admin.RUT'), nullable=False)

    conductor_asignado = db.relationship('Conductor', foreign_keys=[id_conductor], back_populates='asignaciones_admin')
    admin_asigna = db.relationship('Admin', foreign_keys=[id_admin], back_populates='conductores_asignados')