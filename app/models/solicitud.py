from app import db
from datetime import datetime

class Solicitud(db.Model):
    __tablename__ = 'solicitud'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_ambiente = db.Column(db.Integer, db.ForeignKey('ambiente.id'), nullable=True)
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')
    justificacion = db.Column(db.Text, nullable=True)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Solicitud('{self.id_usuario}', '{self.cantidad}', '{self.estado}', '{self.justificacion}', '{self.fecha_solicitud}')"