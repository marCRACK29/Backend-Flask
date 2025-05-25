from app import db

class AdminConductor(db.Model):
    __tablename__ = 'admin_conductor'

    id = db.Column(db.Integer, primary_key=True)
    conductor_id = db.Column(db.String(12), db.ForeignKey('conductor.RUT'), nullable=False)
    admin_id = db.Column(db.String(12), db.ForeignKey('admin.RUT'), nullable=False)

    conductor_asignado = db.relationship('Conductor', foreign_keys=[conductor_id], back_populates='asignaciones_admin')
    admin_asigna = db.relationship('Admin', foreign_keys=[admin_id], back_populates='conductores_asignados')