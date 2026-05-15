from app import db
from datetime import datetime

class Login_auditoria(db.Model):
    __tablename__ = 'login_auditoria'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    email_usuario = db.Column(db.String(120), nullable=False)
    exitoso = db.Column(db.Boolean, nullable=False)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"LoginAuditoria('{self.id_usuario}', '{self.fecha_hora}', '{self.email_usuario}', '{self.exitoso}')"