import os
import sys
import unittest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import db
from app.models.usuario import Usuario
from app.models.rol import Rol
from test.base_test import BaseTestCase


class TestUsuarioModel(BaseTestCase):
    """
    Pruebas unitarias para el modelo Usuario (app/models/usuario.py).

    Contexto en la aplicación:
    El modelo Usuario gestiona la identidad, credenciales y estado de acceso de cada persona
    en la plataforma (administradores, auditores, instructores, aprendices).
    Contempla flags de seguridad como 'aprobado' (requerido para nuevos registros antes de poder
    iniciar sesión) y 'activo' (para suspensión o reactivación de cuentas). Además, se relaciona
    con un Rol para determinar permisos en el sistema.
    """

    def setUp(self):
        super().setUp()
        self.rol_instructor = self.crear_rol(nombre='instructor', descripcion='Rol docente')
        self.rol_admin = self.crear_rol(nombre='admin', descripcion='Rol administrador')

    def test_creacion_usuario_exitosa_y_valores_por_defecto(self):
        """Valida que un usuario se cree con sus atributos y valores por defecto esperados."""
        usuario = Usuario(
            nombre='carlos_sena',
            email='carlos@misena.edu.co',
            password=generate_password_hash('ClaveSegura123'),
            id_rol=self.rol_instructor.id
        )
        db.session.add(usuario)
        db.session.commit()

        self.assertIsNotNone(usuario.id)
        self.assertEqual(usuario.nombre, 'carlos_sena')
        self.assertEqual(usuario.email, 'carlos@misena.edu.co')
        self.assertEqual(usuario.id_rol, self.rol_instructor.id)
        # Valores por defecto del modelo
        self.assertFalse(usuario.aprobado, "Por defecto un nuevo usuario no debe estar aprobado")
        self.assertTrue(usuario.activo, "Por defecto un nuevo usuario debe crearse activo")
        self.assertIsInstance(usuario.creado_en, datetime)

    def test_usuario_email_unico(self):
        """Valida que no se puedan registrar dos usuarios con el mismo correo electrónico."""
        u1 = Usuario(
            nombre='user1',
            email='repetido@correo.com',
            password='hash1',
            id_rol=self.rol_instructor.id
        )
        db.session.add(u1)
        db.session.commit()

        u2 = Usuario(
            nombre='user2',
            email='repetido@correo.com',
            password='hash2',
            id_rol=self.rol_instructor.id
        )
        db.session.add(u2)

        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_usuario_nombre_unico(self):
        """Valida que no se puedan registrar dos usuarios con el mismo nombre de usuario."""
        u1 = Usuario(
            nombre='usuario_duplicado',
            email='uno@correo.com',
            password='hash1',
            id_rol=self.rol_instructor.id
        )
        db.session.add(u1)
        db.session.commit()

        u2 = Usuario(
            nombre='usuario_duplicado',
            email='dos@correo.com',
            password='hash2',
            id_rol=self.rol_instructor.id
        )
        db.session.add(u2)

        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_usuario_campos_obligatorios(self):
        """Valida que campos requeridos como email, password y rol no puedan ser nulos."""
        # Sin password
        u_sin_pass = Usuario(
            nombre='sin_pass',
            email='sinpass@correo.com',
            password=None,
            id_rol=self.rol_instructor.id
        )
        db.session.add(u_sin_pass)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        # Sin id_rol
        u_sin_rol = Usuario(
            nombre='sin_rol',
            email='sinrol@correo.com',
            password='hash',
            id_rol=None
        )
        db.session.add(u_sin_rol)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_flujo_aprobacion_usuario(self):
        """
        Valida el flujo de aprobación del usuario:
        Un usuario registrado inicia con aprobado=False; tras la revisión administrativa,
        se aprueba y se confirma el cambio en la base de datos.
        """
        usuario = Usuario(
            nombre='nuevo_registro',
            email='nuevo@sena.edu.co',
            password=generate_password_hash('password123'),
            id_rol=self.rol_instructor.id,
            aprobado=False
        )
        db.session.add(usuario)
        db.session.commit()

        self.assertFalse(usuario.aprobado)

        # Simular aprobación por parte del administrador
        usuario.aprobado = True
        db.session.commit()

        consultado = db.session.get(Usuario, usuario.id)
        self.assertTrue(consultado.aprobado)

    def test_desactivacion_y_reactivacion_cuenta(self):
        """Valida que una cuenta de usuario pueda ser desactivada (suspendida) y reactivada."""
        usuario = self.crear_usuario(
            nombre='activo_test',
            email='activo@correo.com',
            rol=self.rol_instructor,
            activo=True
        )
        self.assertTrue(usuario.activo)

        # Desactivar cuenta
        usuario.activo = False
        db.session.commit()

        usuario_inactivo = db.session.get(Usuario, usuario.id)
        self.assertFalse(usuario_inactivo.activo)

        # Reactivar cuenta
        usuario.activo = True
        db.session.commit()
        self.assertTrue(db.session.get(Usuario, usuario.id).activo)

    def test_almacenamiento_y_verificacion_hash_password(self):
        """
        Valida que el campo password almacene hashes de longitud adecuada (hasta 256 caracteres)
        y que sea compatible con los algoritmos criptográficos utilizados en la app.
        """
        raw_password = 'MiClaveUltraSegura#2026'
        hashed = generate_password_hash(raw_password)

        usuario = self.crear_usuario(
            nombre='seguro_user',
            email='seguro@correo.com',
            password=hashed,
            rol=self.rol_instructor
        )

        self.assertNotEqual(usuario.password, raw_password)
        self.assertTrue(check_password_hash(usuario.password, raw_password))
        self.assertFalse(check_password_hash(usuario.password, 'clave_incorrecta'))

    def test_usuario_repr(self):
        """Valida la representación en cadena con el formato Usuario('nombre', 'email')."""
        usuario = Usuario(nombre='maria_lopez', email='maria@sena.edu.co')
        self.assertEqual(repr(usuario), "Usuario('maria_lopez', 'maria@sena.edu.co')")


if __name__ == '__main__':
    unittest.main()
