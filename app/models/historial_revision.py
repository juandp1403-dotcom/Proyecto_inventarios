from app import db
from datetime import datetime

class HistorialRevision(db.Model):
    __tablename__ = 'historial_revision'
    id = db.Column(db.Integer, primary_key=True)
    id_ambiente = db.Column(db.Integer, db.ForeignKey('ambiente.id'), nullable=False)
    fecha_revision = db.Column(db.DateTime, default=datetime.utcnow)
    tipo_accion = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    id_referencia = db.Column(db.Integer, nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    
    def __repr__(self):
        return f"HistorialRevision(ambiente:{self.id_ambiente}, fecha:{self.fecha_revision}, tipo:{self.tipo_accion})"
    
    @staticmethod
    def registrar_revision(id_ambiente, tipo_accion, descripcion='', id_referencia=None, id_usuario=None):
        historial = HistorialRevision(
            id_ambiente=id_ambiente,
            tipo_accion=tipo_accion,
            descripcion=descripcion,
            id_referencia=id_referencia,
            id_usuario=id_usuario
        )
        db.session.add(historial)
        db.session.commit()
        return historial
