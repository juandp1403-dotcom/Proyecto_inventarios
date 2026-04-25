from app import db

class SolicitudDetalle(db.Model):
    __tablename__ = 'solicitud_detalle'
    id = db.Column(db.Integer, primary_key=True)
    id_solicitud = db.Column(db.Integer, db.ForeignKey('solicitud.id'), nullable=False)
    id_articulo = db.Column(db.Integer, db.ForeignKey('articulo.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"SolicitudDetalle('{self.id_solicitud}', '{self.id_articulo}', '{self.cantidad}')"