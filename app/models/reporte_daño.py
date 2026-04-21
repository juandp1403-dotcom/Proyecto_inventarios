from app import db
from datetime import datetime

class Reporte_daño(db.Model):
    tablename = 'reporte_dano'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_articulo = db.Column(db.Integer, db.ForeignKey('articulo.id'), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    gravedad = db.Column(db.String(20), nullable=False)  # 'leve', 'moderado', 'grave'
    evidencia = db.Column(db.String(200), nullable=True)  # URL o ruta de la evidencia
    estado = db.Column(db.String(20), nullable=False, default='pendiente')  # 'pendiente', 'en revisión', 'resuelto'
    fecha_reporte = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Reporte_daño('{self.descripcion}', '{self.gravedad}', '{self.estado}', '{self.fecha_reporte}')"