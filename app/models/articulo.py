from app import db
from datetime import datetime

class Articulo(db.Model):
    tablename = 'articulo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    nivel_minimo = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(200), nullable=True)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Articulo('{self.nombre}', '{self.fecha_publicacion}')"