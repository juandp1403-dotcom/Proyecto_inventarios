import os
import sys
import unittest
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import db
from app.models.login_auditoria import Login_auditoria
from app.models.usuario import Usuario
from test.base_test import BaseTestCase


class TestLoginAuditoriaModel(BaseTestCase):
    """
    Pruebas unitarias para el modelo Login_auditoria (app/models/login_auditoria.py).

    Contexto en la aplicación:
    El modelo Login_auditoria es un pilar crítico de la seguridad informática del sistema.
    Cada vez que un usuario intenta autenticarse mediante la ruta '/login'
    (función 'record_audit_login' en app/routes/usuario_routes.py), se registra de forma inmutable:
    el usuario involucrado, el correo ingresado, si el inicio de sesión fue exitoso o fallido,
    y la marca de tiempo (timestamp).
    Permite auditar eventos de seguridad, detectar ataques de fuerza bruta y conservar
    trazabilidad forense de los accesos al sistema.
    """

    def setUp(self):
        super().setUp()
        self.rol = self.crear_rol(nombre='auditor', descripcion='Rol de auditoría')
        self.usuario = self.crear_usuario(
            nombre='auditor_user',
            email='auditor@sena.edu.co',
            rol=self.rol
        )

    def test_registro_login_exitoso(self):
        """Valida el registro correcto de un intento de autenticación exitoso."""
        registro = Login_auditoria(
            id_usuario=self.usuario.id,
            email_usuario=self.usuario.email,
            exitoso=True
        )
        db.session.add(registro)
        db.session.commit()

        self.assertIsNotNone(registro.id)
        self.assertEqual(registro.id_usuario, self.usuario.id)
        self.assertEqual(registro.email_usuario, 'auditor@sena.edu.co')
        self.assertTrue(registro.exitoso)
        self.assertIsInstance(registro.fecha_hora, datetime)

    def test_registro_login_fallido(self):
        """Valida el registro de una autenticación fallida (contraseña errónea o cuenta no aprobada)."""
        registro = Login_auditoria(
            id_usuario=self.usuario.id,
            email_usuario=self.usuario.email,
            exitoso=False
        )
        db.session.add(registro)
        db.session.commit()

        guardado = db.session.get(Login_auditoria, registro.id)
        self.assertIsNotNone(guardado)
        self.assertFalse(guardado.exitoso)

    def test_campos_obligatorios(self):
        """Valida que id_usuario, email_usuario y exitoso no permitan valores nulos."""
        # Sin id_usuario
        sin_usuario = Login_auditoria(id_usuario=None, email_usuario='test@correo.com', exitoso=True)
        db.session.add(sin_usuario)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        # Sin email_usuario
        sin_email = Login_auditoria(id_usuario=self.usuario.id, email_usuario=None, exitoso=True)
        db.session.add(sin_email)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        # Sin exitoso
        sin_exitoso = Login_auditoria(id_usuario=self.usuario.id, email_usuario='test@correo.com', exitoso=None)
        db.session.add(sin_exitoso)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_fecha_hora_automatica(self):
        """Valida que la fecha y hora se asignen automáticamente al momento del registro."""
        antes = datetime.utcnow() - timedelta(seconds=2)
        registro = Login_auditoria(
            id_usuario=self.usuario.id,
            email_usuario=self.usuario.email,
            exitoso=True
        )
        db.session.add(registro)
        db.session.commit()
        despues = datetime.utcnow() + timedelta(seconds=2)

        self.assertTrue(antes <= registro.fecha_hora <= despues)

    def test_trazabilidad_y_conteo_intentos_fallidos(self):
        """
        Valida que se puedan consultar y contabilizar los intentos fallidos de un usuario,
        contexto clave para detección de intrusiones o políticas de bloqueo de cuenta.
        """
        # Registrar 3 intentos fallidos y 1 exitoso
        for _ in range(3):
            db.session.add(Login_auditoria(
                id_usuario=self.usuario.id,
                email_usuario=self.usuario.email,
                exitoso=False
            ))
        db.session.add(Login_auditoria(
            id_usuario=self.usuario.id,
            email_usuario=self.usuario.email,
            exitoso=True
        ))
        db.session.commit()

        fallidos = Login_auditoria.query.filter_by(id_usuario=self.usuario.id, exitoso=False).count()
        exitosos = Login_auditoria.query.filter_by(id_usuario=self.usuario.id, exitoso=True).count()

        self.assertEqual(fallidos, 3)
        self.assertEqual(exitosos, 1)

    def test_simulacion_funcion_record_audit_login(self):
        """
        Simula la lógica exacta de la función 'record_audit_login' empleada en 'app/routes/usuario_routes.py'
        para verificar la integración directa del modelo en el flujo de negocio.
        """
        def record_audit_login_mock(user_id, email, success):
            login = Login_auditoria(
                id_usuario=user_id,
                email_usuario=email,
                exitoso=success
            )
            db.session.add(login)
            db.session.commit()
            return login

        registro = record_audit_login_mock(self.usuario.id, self.usuario.email, True)
        self.assertIsNotNone(registro.id)
        self.assertTrue(registro.exitoso)
        self.assertEqual(registro.email_usuario, self.usuario.email)

    def test_login_auditoria_repr(self):
        """Valida que __repr__ retorne la cadena esperada con los atributos del modelo."""
        fecha_fija = datetime(2026, 6, 15, 10, 30, 0)
        registro = Login_auditoria(
            id_usuario=self.usuario.id,
            email_usuario='test@sena.edu.co',
            exitoso=True,
            fecha_hora=fecha_fija
        )
        esperado = f"LoginAuditoria('{self.usuario.id}', '{fecha_fija}', 'test@sena.edu.co', 'True')"
        self.assertEqual(repr(registro), esperado)


if __name__ == '__main__':
    unittest.main()
