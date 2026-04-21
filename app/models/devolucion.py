from app import db
from datetime import datetime

class Devolucion(db.Model):
    tablename = 'devolucion'
    id = db.Column(db.Integer, primary_key=True)
    id_solicitud = db.Column(db.Integer, db.ForeignKey('solicitud.id'), nullable=False)
    estado_elemento = db.Column(db.String(20), nullable=False)  # 'bueno', 'dañado', 'perdido'
    observacion = db.Column(db.Text, nullable=True)
    fecha_devolucion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Devolucion('{self.estado_elemento}', '{self.fecha_devolucion}', '{self.observacion}')'"