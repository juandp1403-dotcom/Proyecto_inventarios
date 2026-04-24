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
    def crear_alerta(titulo, mensaje, tipo, id_usuario_destino=None, id_referencia=None):
        from app.models.usuario import Usuario
        from app.models.rol import Rol
        
        # Si no se especifica destino, enviar a todos los admin y auditor
        if id_usuario_destino is None:
            admin_rol = Rol.query.filter_by(nombre='admin').first()
            auditor_rol = Rol.query.filter_by(nombre='auditor').first()
            
            # Enviar a todos los usuarios admin
            if admin_rol:
                admin_users = Usuario.query.filter_by(id_rol=admin_rol.id).all()
                for user in admin_users:
                    alerta = Alerta(
                        titulo=titulo,
                        mensaje=mensaje,
                        tipo=tipo,
                        id_usuario_destino=user.id,
                        id_referencia=id_referencia
                    )
                    db.session.add(alerta)
            
            # Enviar a todos los usuarios auditor
            if auditor_rol:
                auditor_users = Usuario.query.filter_by(id_rol=auditor_rol.id).all()
                for user in auditor_users:
                    alerta = Alerta(
                        titulo=titulo,
                        mensaje=mensaje,
                        tipo=tipo,
                        id_usuario_destino=user.id,
                        id_referencia=id_referencia
                    )
                    db.session.add(alerta)
        else:
            # Enviar a un usuario específico
            alerta = Alerta(
                titulo=titulo,
                mensaje=mensaje,
                tipo=tipo,
                id_usuario_destino=id_usuario_destino,
                id_referencia=id_referencia
            )
            db.session.add(alerta)
        
        db.session.commit()
        if id_usuario_destino is None:
            return None
        return alerta