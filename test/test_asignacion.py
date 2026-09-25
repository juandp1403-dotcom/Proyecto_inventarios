import os
import sys
import unittest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import db
from app.models.asignacion import Asignacion
from test.base_test import BaseTestCase


class TestAsignacionModel(BaseTestCase):
    """Pruebas unitarias para el modelo Asignacion."""

    def setUp(self):
        super().setUp()
        rol = self.crear_rol(nombre='instructor')
        self.usuario = self.crear_usuario(
            nombre='instructor_asignacion',
            email='instructor.asignacion@sena.edu.co',
            rol=rol
        )
        self.articulo = self.crear_articulo(nombre='Kit Arduino', codigo='ELEC-030')
        self.ambiente = self.crear_ambiente(nombre='Laboratorio de Robótica')

    def test_crear_asignacion(self):
        asignacion = Asignacion(
            id_usuario=self.usuario.id,
            id_articulo=self.articulo.id,
            id_ambiente=self.ambiente.id,
            cantidad=2
        )
        db.session.add(asignacion)
        db.session.commit()

        guardada = db.session.get(Asignacion, asignacion.id)
        self.assertIsNotNone(guardada)
        self.assertEqual(guardada.id_usuario, self.usuario.id)
        self.assertEqual(guardada.id_articulo, self.articulo.id)
        self.assertEqual(guardada.id_ambiente, self.ambiente.id)
        self.assertEqual(guardada.cantidad, 2)
        self.assertIsInstance(guardada.fecha_asignacion, datetime)

    def test_asignacion_campos_obligatorios(self):
        asignacion = Asignacion(
            id_usuario=self.usuario.id,
            id_articulo=self.articulo.id,
            id_ambiente=None,
            cantidad=1
        )
        db.session.add(asignacion)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_fecha_asignacion_predeterminada(self):
        asignacion = Asignacion(
            id_usuario=self.usuario.id,
            id_articulo=self.articulo.id,
            id_ambiente=self.ambiente.id,
            cantidad=1
        )
        db.session.add(asignacion)
        db.session.commit()

        guardada = db.session.get(Asignacion, asignacion.id)
        self.assertIsInstance(guardada.fecha_asignacion, datetime)

    def test_consultar_asignaciones_por_ambiente(self):
        db.session.add_all([
            Asignacion(
                id_usuario=self.usuario.id,
                id_articulo=self.articulo.id,
                id_ambiente=self.ambiente.id,
                cantidad=1
            ),
            Asignacion(
                id_usuario=self.usuario.id,
                id_articulo=self.articulo.id,
                id_ambiente=self.ambiente.id,
                cantidad=3
            )
        ])
        db.session.commit()

        asignaciones = Asignacion.query.filter_by(id_ambiente=self.ambiente.id).all()
        self.assertEqual(len(asignaciones), 2)
        self.assertEqual(sum(asignacion.cantidad for asignacion in asignaciones), 4)

    def test_asignacion_repr(self):
        fecha_fija = datetime(2026, 5, 12, 9, 30, 0)
        asignacion = Asignacion(
            id_usuario=self.usuario.id,
            id_articulo=self.articulo.id,
            id_ambiente=self.ambiente.id,
            cantidad=2,
            fecha_asignacion=fecha_fija
        )
        esperado = (
            f"Asignacion('{self.usuario.id}', '{self.articulo.id}', "
            f"'{self.ambiente.id}', '2', '{fecha_fija}')"
        )
        self.assertEqual(repr(asignacion), esperado)


if __name__ == '__main__':
    unittest.main()