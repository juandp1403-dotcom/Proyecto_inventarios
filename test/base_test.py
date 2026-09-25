import os
import sys
import unittest

# Asegurar que la raíz del proyecto esté en sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Configurar variables de entorno antes de cargar la aplicación
os.environ['SECRET_KEY'] = 'test-secret-key-12345'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import create_app, db
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.ambiente import Ambiente
from app.models.categoria import Categoria
from app.models.articulo import Articulo


class BaseTestCase(unittest.TestCase):
    """
    Clase base para pruebas unitarias de los modelos del sistema de inventarios.
    Configura una base de datos SQLite en memoria aislada para cada prueba,
    garantizando que las pruebas sean independientes y no alteren los datos reales.
    """

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def crear_rol(self, nombre='admin', descripcion='Rol de administración'):
        """Helper para registrar un rol en el contexto de control de acceso."""
        rol = Rol(nombre=nombre, descripcion=descripcion)
        db.session.add(rol)
        db.session.commit()
        return rol

    def crear_usuario(self, nombre='testuser', email='test@correo.com', password='hashed_password_123', rol=None, aprobado=True, activo=True):
        """Helper para registrar un usuario asociado a un rol."""
        if rol is None:
            rol = self.crear_rol()
        usuario = Usuario(
            nombre=nombre,
            email=email,
            password=password,
            id_rol=rol.id,
            aprobado=aprobado,
            activo=activo
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario

    def crear_ambiente(self, nombre='Ambiente de Sistemas', tipo='Laboratorio', ubicacion='Torre 1 Piso 2'):
        """Helper para registrar un ambiente donde se ubican o asignan recursos."""
        ambiente = Ambiente(
            nombre=nombre,
            tipo=tipo,
            ubicacion=ubicacion,
            descripcion='Ambiente de formación técnica'
        )
        db.session.add(ambiente)
        db.session.commit()
        return ambiente

    def crear_articulo(self, nombre='Portátil Lenovo', codigo='ART-001', categoria_id=None, cantidad=15, estado='Disponible', nivel_minimo=3):
        """Helper para registrar un artículo en el inventario."""
        if categoria_id is None:
            categoria = Categoria(nombre='Equipos de Cómputo')
            db.session.add(categoria)
            db.session.commit()
            categoria_id = categoria.id

        articulo = Articulo(
            nombre=nombre,
            codigo=codigo,
            descripcion='Portátil institucional para formación',
            id_categoria=categoria_id,
            cantidad=cantidad,
            estado=estado,
            nivel_minimo=nivel_minimo
        )
        db.session.add(articulo)
        db.session.commit()
        return articulo
