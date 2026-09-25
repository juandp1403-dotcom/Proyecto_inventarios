import os
import sys
import unittest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import db
from app.models.solicitud import Solicitud
from test.base_test import BaseTestCase


class TestSolicitudModel(BaseTestCase):
    """
    Pruebas unitarias para el modelo Solicitud (app/models/solicitud.py).

    Contexto en la aplicación:
    El modelo Solicitud gestiona el flujo de requerimiento y préstamo de recursos e insumos.
    Los instructores o aprendices radican solicitudes de material justificando la necesidad
    para un ambiente específico ('Ambiente').
    La solicitud nace en estado 'pendiente' y posteriormente los administradores o auditores
    la gestionan mediante las rutas '/<id>/aprobar' o '/<id>/rechazar' (en app/routes/solicitud_routes.py).
    Posee relaciones bidireccionales con 'Usuario' (solicitante) y 'Ambiente' (destino).
    """

    def setUp(self):
        super().setUp()
        self.rol_aprendiz = self.crear_rol(nombre='aprendiz', descripcion='Rol aprendiz')
        self.rol_admin = self.crear_rol(nombre='admin', descripcion='Rol administrador')

        self.usuario_solicitante = self.crear_usuario(
            nombre='aprendiz_andres',
            email='andres@misena.edu.co',
            rol=self.rol_aprendiz
        )
        self.ambiente = self.crear_ambiente(
            nombre='Taller de Redes',
            tipo='Laboratorio de Telecomunicaciones'
        )

    def test_creacion_solicitud_exitosa_y_valores_por_defecto(self):
        """Valida que una solicitud se registre con estado 'pendiente' por defecto."""
        solicitud = Solicitud(
            id_usuario=self.usuario_solicitante.id,
            id_ambiente=self.ambiente.id,
            cantidad=3,
            justificacion='Se requieren cables y routers para práctica final'
        )
        db.session.add(solicitud)
        db.session.commit()

        self.assertIsNotNone(solicitud.id)
        self.assertEqual(solicitud.id_usuario, self.usuario_solicitante.id)
        self.assertEqual(solicitud.id_ambiente, self.ambiente.id)
        self.assertEqual(solicitud.cantidad, 3)
        self.assertEqual(solicitud.estado, 'pendiente')
        self.assertEqual(solicitud.justificacion, 'Se requieren cables y routers para práctica final')
        self.assertIsInstance(solicitud.fecha_solicitud, datetime)

    def test_relaciones_bidireccionales_usuario_y_ambiente(self):
        """
        Valida que se pueda navegar desde Solicitud hacia Usuario y Ambiente,
        así como desde Usuario.solicitudes y Ambiente.solicitudes (backrefs).
        """
        solicitud = Solicitud(
            id_usuario=self.usuario_solicitante.id,
            id_ambiente=self.ambiente.id,
            cantidad=1,
            justificacion='Módulo de prueba'
        )
        db.session.add(solicitud)
        db.session.commit()

        # Acceso directo
        self.assertEqual(solicitud.usuario.nombre, 'aprendiz_andres')
        self.assertEqual(solicitud.ambiente.nombre, 'Taller de Redes')

        # Acceso inverso mediante backref
        self.assertIn(solicitud, self.usuario_solicitante.solicitudes)
        self.assertIn(solicitud, self.ambiente.solicitudes)

    def test_flujo_transicion_estado_aprobacion(self):
        """
        Valida el flujo de aprobación gestionado en 'solicitud_routes.aprobar_solicitud':
        El estado pasa de 'pendiente' a 'aprobada'.
        """
        solicitud = Solicitud(
            id_usuario=self.usuario_solicitante.id,
            id_ambiente=self.ambiente.id,
            cantidad=2,
            justificacion='Préstamo de multímetros'
        )
        db.session.add(solicitud)
        db.session.commit()

        self.assertEqual(solicitud.estado, 'pendiente')

        # Acción de aprobación
        solicitud.estado = 'aprobada'
        db.session.commit()

        actualizada = db.session.get(Solicitud, solicitud.id)
        self.assertEqual(actualizada.estado, 'aprobada')

    def test_flujo_transicion_estado_rechazo(self):
        """
        Valida el flujo de rechazo gestionado en 'solicitud_routes.rechazar_solicitud':
        El estado pasa de 'pendiente' a 'rechazada'.
        """
        solicitud = Solicitud(
            id_usuario=self.usuario_solicitante.id,
            id_ambiente=self.ambiente.id,
            cantidad=10,
            justificacion='Cantidad excede disponibilidad'
        )
        db.session.add(solicitud)
        db.session.commit()

        # Acción de rechazo
        solicitud.estado = 'rechazada'
        db.session.commit()

        actualizada = db.session.get(Solicitud, solicitud.id)
        self.assertEqual(actualizada.estado, 'rechazada')

    def test_solicitud_campos_obligatorios(self):
        """Valida que id_usuario y cantidad sean campos obligatorios."""
        # Sin id_usuario
        s_sin_user = Solicitud(id_usuario=None, cantidad=1)
        db.session.add(s_sin_user)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        # Sin cantidad
        s_sin_cant = Solicitud(id_usuario=self.usuario_solicitante.id, cantidad=None)
        db.session.add(s_sin_cant)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_solicitud_ambiente_opcional(self):
        """Valida que una solicitud pueda crearse sin asociar un ambiente específico (id_ambiente=None)."""
        solicitud = Solicitud(
            id_usuario=self.usuario_solicitante.id,
            id_ambiente=None,
            cantidad=1,
            justificacion='Solicitud de material para formación virtual'
        )
        db.session.add(solicitud)
        db.session.commit()

        guardada = db.session.get(Solicitud, solicitud.id)
        self.assertIsNotNone(guardada)
        self.assertIsNone(guardada.id_ambiente)
        self.assertIsNone(guardada.ambiente)

    def test_filtrado_solicitudes_por_estado(self):
        """
        Valida el filtrado de solicitudes por estado para paneles de control
        y reportes de gestión de inventarios.
        """
        s1 = Solicitud(id_usuario=self.usuario_solicitante.id, cantidad=1, estado='pendiente')
        s2 = Solicitud(id_usuario=self.usuario_solicitante.id, cantidad=2, estado='aprobada')
        s3 = Solicitud(id_usuario=self.usuario_solicitante.id, cantidad=3, estado='rechazada')
        db.session.add_all([s1, s2, s3])
        db.session.commit()

        pendientes = Solicitud.query.filter_by(estado='pendiente').all()
        aprobadas = Solicitud.query.filter_by(estado='aprobada').all()
        rechazadas = Solicitud.query.filter_by(estado='rechazada').all()

        self.assertEqual(len(pendientes), 1)
        self.assertEqual(len(aprobadas), 1)
        self.assertEqual(len(rechazadas), 1)

    def test_solicitud_repr(self):
        """Valida el método __repr__ de Solicitud."""
        fecha_fija = datetime(2026, 5, 1, 14, 0, 0)
        solicitud = Solicitud(
            id_usuario=self.usuario_solicitante.id,
            cantidad=4,
            estado='pendiente',
            justificacion='Kits arduino',
            fecha_solicitud=fecha_fija
        )
        esperado = f"Solicitud('{self.usuario_solicitante.id}', '4', 'pendiente', 'Kits arduino', '{fecha_fija}')"
        self.assertEqual(repr(solicitud), esperado)


if __name__ == '__main__':
    unittest.main()
