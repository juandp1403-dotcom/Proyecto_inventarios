import os
import sys
import unittest
from sqlalchemy.exc import IntegrityError

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import db
from app.models.articulo_caracteristica import Articulo_caracteristica
from app.models.caracteristica import Caracteristica
from test.base_test import BaseTestCase


class TestArticuloCaracteristicaModel(BaseTestCase):
    """Pruebas unitarias para la asociación entre artículos y características."""

    def setUp(self):
        super().setUp()
        self.articulo = self.crear_articulo()
        self.caracteristica = Caracteristica(
            nombre='Memoria RAM',
            descripcion='Capacidad de memoria instalada'
        )
        db.session.add(self.caracteristica)
        db.session.commit()

    def test_asociar_articulo_y_caracteristica(self):
        asociacion = Articulo_caracteristica(
            id_articulo=self.articulo.id,
            id_caracteristica=self.caracteristica.id
        )
        db.session.add(asociacion)
        db.session.commit()

        guardada = db.session.get(Articulo_caracteristica, asociacion.id)
        self.assertIsNotNone(guardada)
        self.assertEqual(guardada.id_articulo, self.articulo.id)
        self.assertEqual(guardada.id_caracteristica, self.caracteristica.id)

    def test_asociacion_campos_obligatorios(self):
        asociacion = Articulo_caracteristica(
            id_articulo=None,
            id_caracteristica=self.caracteristica.id
        )
        db.session.add(asociacion)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_consultar_caracteristicas_asociadas_por_articulo(self):
        segunda = Caracteristica(nombre='Procesador', descripcion='Modelo del procesador')
        db.session.add(segunda)
        db.session.flush()
        db.session.add_all([
            Articulo_caracteristica(
                id_articulo=self.articulo.id,
                id_caracteristica=self.caracteristica.id
            ),
            Articulo_caracteristica(
                id_articulo=self.articulo.id,
                id_caracteristica=segunda.id
            )
        ])
        db.session.commit()

        asociaciones = Articulo_caracteristica.query.filter_by(
            id_articulo=self.articulo.id
        ).all()
        self.assertEqual(len(asociaciones), 2)
        self.assertEqual(
            {asociacion.id_caracteristica for asociacion in asociaciones},
            {self.caracteristica.id, segunda.id}
        )

    def test_asociacion_repr(self):
        asociacion = Articulo_caracteristica(
            id_articulo=self.articulo.id,
            id_caracteristica=self.caracteristica.id
        )
        esperado = f"ArticuloCaracteristica('{self.articulo.id}', '{self.caracteristica.id}')"
        self.assertEqual(repr(asociacion), esperado)


if __name__ == '__main__':
    unittest.main()