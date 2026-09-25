import os
import sys
import unittest
from sqlalchemy.exc import IntegrityError

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import db
from app.models.ambiente import Ambiente
from test.base_test import BaseTestCase


class TestAmbienteModel(BaseTestCase):
    """Pruebas unitarias para el modelo Ambiente."""

    def test_crear_ambiente_y_campos_opcionales(self):
        ambiente = Ambiente(
            nombre='Laboratorio de Redes',
            tipo='Laboratorio',
            ubicacion=None,
            descripcion=None
        )
        db.session.add(ambiente)
        db.session.commit()

        guardado = db.session.get(Ambiente, ambiente.id)
        self.assertIsNotNone(guardado)
        self.assertEqual(guardado.nombre, 'Laboratorio de Redes')
        self.assertEqual(guardado.tipo, 'Laboratorio')
        self.assertIsNone(guardado.ubicacion)
        self.assertIsNone(guardado.descripcion)

    def test_ambiente_campos_obligatorios(self):
        ambiente = Ambiente(nombre=None, tipo='Laboratorio')
        db.session.add(ambiente)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_nombre_ambiente_unico(self):
        self.crear_ambiente(nombre='Taller de Electrónica')
        duplicado = Ambiente(nombre='Taller de Electrónica', tipo='Taller')
        db.session.add(duplicado)

        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_consultar_ambiente_por_nombre(self):
        self.crear_ambiente(nombre='Aula de Automatización')

        ambiente = Ambiente.query.filter_by(nombre='Aula de Automatización').first()
        self.assertIsNotNone(ambiente)
        self.assertEqual(ambiente.tipo, 'Laboratorio')

    def test_ambiente_repr(self):
        ambiente = Ambiente(nombre='Aula de Diseño', tipo='Aula')
        self.assertEqual(repr(ambiente), "Ambiente('Aula de Diseño')")


if __name__ == '__main__':
    unittest.main()