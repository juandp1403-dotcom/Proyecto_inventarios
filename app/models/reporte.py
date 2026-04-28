from app import db
from datetime import datetime

class Reporte(db.Model):
    __tablename__ = 'reporte'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    filtros = db.Column(db.Text, nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_ambiente = db.Column(db.Integer, db.ForeignKey('ambiente.id'), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    ambiente = db.relationship('Ambiente', backref='reportes')
    usuario = db.relationship('Usuario', backref='reportes')
    
    def __repr__(self):
        return f"Reporte('{self.tipo}', '{self.filtros}', '{self.fecha_creacion}')"