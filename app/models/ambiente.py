from app import db

class Ambiente(db.Model):
    tablename = 'ambiente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    ubicacion = db.Column(db.String(200), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Ambiente('{self.nombre}')"