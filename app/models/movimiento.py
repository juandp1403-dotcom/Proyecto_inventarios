from app import db
from datetime import datetime

class Movimiento(db.Model):
    __tablename__ = 'movimiento'
    id = db.Column(db.Integer, primary_key=True)
    id_articulo = db.Column(db.Integer, db.ForeignKey('articulo.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'entrada' o 'salida'
    cantidad = db.Column(db.Integer, nullable=False)
    observacion = db.Column(db.Text, nullable=True)
    fecha_movimiento = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Movimiento('{self.tipo}', '{self.cantidad}', '{self.fecha_movimiento}', '{self.observacion}')"