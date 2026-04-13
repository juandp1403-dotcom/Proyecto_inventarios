from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Cargar configuración
    app.config.from_object('config.Config')

    db.init_app(app)

    # Importar modelos (IMPORTANTE)
    from app.models import *

    return app