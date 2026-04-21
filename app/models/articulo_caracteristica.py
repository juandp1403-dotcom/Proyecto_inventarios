from app import db

class Articulo_caracteristica(db.Model):
    tablename = 'articulo_caracteristica'
    id = db.Column(db.Integer, primary_key=True)
    id_articulo = db.Column(db.Integer, db.ForeignKey('articulo.id'), nullable=False)
    id_caracteristica = db.Column(db.Integer, db.ForeignKey('caracteristica.id'), nullable=False)

    def __repr__(self):
        return f"ArticuloCaracteristica('{self.id_articulo}', '{self.id_caracteristica}')"