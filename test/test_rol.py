import os
import sys
import unittest
from sqlalchemy.exc import IntegrityError

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import db
from app.models.rol import Rol
from test.base_test import BaseTestCase


class TestRolModel(BaseTestCase):
    """
    Pruebas unitarias para el modelo Rol (app/models/rol.py).

    Contexto en la aplicación:
    El modelo Rol es la base del control de acceso basado en roles (RBAC) del sistema.
    Define los perfiles de usuario ('admin', 'auditor', 'revisor', 'instructor', 'aprendiz')
    que controlan los permisos en las rutas mediante decoradores (@role_required) y determinan
    las acciones permitidas (gestión de inventario, aprobación de solicitudes, auditoría, etc.).
    """

    def test_creacion_rol_exitosa(self):
        """Valida que un rol con nombre y descripción se registre correctamente."""
        rol = Rol(nombre='admin', descripcion='Administrador del sistema con control total')
        db.session.add(rol)
        db.session.commit()

        self.assertIsNotNone(rol.id)
        self.assertEqual(rol.nombre, 'admin')
        self.assertEqual(rol.descripcion, 'Administrador del sistema con control total')

    def test_rol_nombre_unico(self):
        """Valida que no se puedan registrar dos roles con el mismo nombre (columna unique=True)."""
        rol1 = Rol(nombre='instructor', descripcion='Rol docente')
        db.session.add(rol1)
        db.session.commit()

        rol2 = Rol(nombre='instructor', descripcion='Duplicado de rol docente')
        db.session.add(rol2)

        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_rol_nombre_requerido(self):
        """Valida que el nombre de rol sea obligatorio (nullable=False)."""
        rol = Rol(nombre=None, descripcion='Rol sin nombre')
        db.session.add(rol)

        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_rol_descripcion_opcional(self):
        """Valida que la descripción sea opcional (nullable=True)."""
        rol = Rol(nombre='auditor', descripcion=None)
        db.session.add(rol)
        db.session.commit()

        guardado = Rol.query.filter_by(nombre='auditor').first()
        self.assertIsNotNone(guardado)
        self.assertIsNone(guardado.descripcion)

    def test_roles_del_sistema_permitidos(self):
        """
        Valida que todos los roles utilizados por las rutas y políticas de acceso
        de la aplicación puedan coexistir y consultarse en la base de datos.
        """
        roles_esperados = ['admin', 'auditor', 'revisor', 'instructor', 'aprendiz']
        for nombre_rol in roles_esperados:
            db.session.add(Rol(nombre=nombre_rol, descripcion=f'Perfil de {nombre_rol}'))
        db.session.commit()

        total = Rol.query.count()
        self.assertEqual(total, len(roles_esperados))

        for nombre_rol in roles_esperados:
            rol = Rol.query.filter_by(nombre=nombre_rol).first()
            self.assertIsNotNone(rol)
            self.assertEqual(rol.nombre, nombre_rol)

    def test_rol_repr(self):
        """Valida que el método __repr__ retorne la cadena esperada con el formato Rol('nombre')."""
        rol = Rol(nombre='revisor')
        self.assertEqual(repr(rol), "Rol('revisor')")

    def test_actualizar_descripcion_rol(self):
        """Valida que la descripción de un rol pueda ser actualizada posteriormente."""
        rol = Rol(nombre='aprendiz', descripcion='Descripción previa')
        db.session.add(rol)
        db.session.commit()

        rol.descripcion = 'Acceso a consulta de catálogo y realización de solicitudes'
        db.session.commit()

        rol_actualizado = db.session.get(Rol, rol.id)
        self.assertEqual(rol_actualizado.descripcion, 'Acceso a consulta de catálogo y realización de solicitudes')


if __name__ == '__main__':
    unittest.main()
