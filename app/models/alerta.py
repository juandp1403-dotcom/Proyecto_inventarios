from app import db
from datetime import datetime

class Alerta(db.Model):
    __tablename__ = 'alerta'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'inventario', 'solicitud', 'reporte', 'devolucion', 'ambiente'
    id_usuario_destino = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_referencia = db.Column(db.Integer, nullable=True)  # ID del elemento relacionado
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    leida = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Alerta('{self.titulo}')"

    @staticmethod
    def crear_alerta(titulo, mensaje, tipo, id_usuario_destino, id_referencia=None):
        alerta = Alerta(
            titulo=titulo,
            mensaje=mensaje,
            tipo=tipo,
            id_usuario_destino=id_usuario_destino,
            id_referencia=id_referencia
        )
        db.session.add(alerta)
        db.session.commit()
        return alerta