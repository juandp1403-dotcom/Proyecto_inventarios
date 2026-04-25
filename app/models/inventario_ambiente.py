from app import db
from datetime import datetime

class InventarioAmbiente(db.Model):
    __tablename__ = 'inventario_ambiente'
    id = db.Column(db.Integer, primary_key=True)
    id_ambiente = db.Column(db.Integer, db.ForeignKey('ambiente.id'), nullable=False)
    id_articulo = db.Column(db.Integer, db.ForeignKey('articulo.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=0)
    cantidad_minima = db.Column(db.Integer, default=2)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"InventarioAmbiente(ambiente:{self.id_ambiente}, articulo:{self.id_articulo}, cantidad:{self.cantidad})"