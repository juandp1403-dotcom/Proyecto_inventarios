from app import db

class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Rol('{self.nombre}')"