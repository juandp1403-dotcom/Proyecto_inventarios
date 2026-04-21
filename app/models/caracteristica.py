from app import db

class Caracteristica(db.Model):
    tablename = 'caracteristica'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Caracteristica('{self.nombre}')"