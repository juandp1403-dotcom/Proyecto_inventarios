from app import db
from datetime import datetime

class Usuario(db.Model):
    tablename = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)
    aprobado = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Usuario('{self.nombre}', '{self.email}')"