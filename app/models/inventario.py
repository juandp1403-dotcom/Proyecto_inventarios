from app import db

class Inventario(db.Model):
    __tablename__ = 'inventario'
    id = db.Column(db.Integer, primary_key=True)
    id_ambiente = db.Column(db.Integer, db.ForeignKey('ambiente.id'), nullable=False)
    id_articulo = db.Column(db.Integer, db.ForeignKey('articulo.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    cantidad_minima = db.Column(db.Integer, nullable=False)
    ultima_actualizacion = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"Inventario(Ambiente:{self.id_ambiente}, Artículo:{self.id_articulo}, Cantidad:{self.cantidad})"
