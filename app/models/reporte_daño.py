from app import db
from datetime import datetime

class Reporte_daño(db.Model):
    __tablename__ = 'reporte_dano'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_articulo = db.Column(db.Integer, db.ForeignKey('articulo.id'), nullable=False)
    id_ambiente = db.Column(db.Integer, db.ForeignKey('ambiente.id'), nullable=True)
    descripcion = db.Column(db.Text, nullable=False)
    gravedad = db.Column(db.String(20), nullable=False)
    evidencia = db.Column(db.String(200), nullable=True)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')
    fecha_reporte = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Reporte_daño('{self.descripcion}', '{self.gravedad}', '{self.estado}', '{self.fecha_reporte}')"