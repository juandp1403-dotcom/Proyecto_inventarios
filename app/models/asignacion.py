from app import db
from datetime import datetime

class Asignacion(db.Model):
    __tablename__ = 'asignacion'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_articulo = db.Column(db.Integer, db.ForeignKey('articulo.id'), nullable=False)
    id_ambiente = db.Column(db.Integer, db.ForeignKey('ambiente.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_asignacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Asignacion('{self.id_usuario}', '{self.id_articulo}', '{self.id_ambiente}', '{self.cantidad}', '{self.fecha_asignacion}')"