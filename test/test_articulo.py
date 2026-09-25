import os
import sys
import unittest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import db
from app.models.articulo import Articulo
from test.base_test import BaseTestCase


class TestArticuloModel(BaseTestCase):
    """Pruebas unitarias para el modelo Articulo."""

    def setUp(self):
        super().setUp()
        self.articulo = self.crear_articulo(
            nombre='Impresora 3D',
            codigo='IMP-003',
            cantidad=4,
            nivel_minimo=1
        )

    def test_crear_articulo_y_persistir_datos(self):
        guardado = db.session.get(Articulo, self.articulo.id)

        self.assertIsNotNone(guardado)
        self.assertEqual(guardado.nombre, 'Impresora 3D')
        self.assertEqual(guardado.codigo, 'IMP-003')
        self.assertEqual(guardado.cantidad, 4)
        self.assertEqual(guardado.nivel_minimo, 1)
        self.assertEqual(guardado.estado, 'Disponible')
        self.assertIsInstance(guardado.fecha_publicacion, datetime)

    def test_articulo_campos_obligatorios(self):
        articulo = Articulo(
            nombre=None,
            codigo='ART-002',
            id_categoria=self.articulo.id_categoria,
            cantidad=1,
            estado='Disponible',
            nivel_minimo=0
        )
        db.session.add(articulo)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_descripcion_e_imagen_opcionales_y_fecha_predeterminada(self):
        articulo = Articulo(
            nombre='Multímetro',
            codigo='ELEC-021',
            id_categoria=self.articulo.id_categoria,
            cantidad=2,
            estado='Disponible',
            nivel_minimo=1,
            descripcion=None,
            imagen=None
        )
        db.session.add(articulo)
        db.session.commit()

        guardado = db.session.get(Articulo, articulo.id)
        self.assertIsNone(guardado.descripcion)
        self.assertIsNone(guardado.imagen)
        self.assertIsInstance(guardado.fecha_publicacion, datetime)

    def test_consultar_articulos_por_categoria(self):
        articulos = Articulo.query.filter_by(id_categoria=self.articulo.id_categoria).all()
        self.assertEqual(len(articulos), 1)
        self.assertEqual(articulos[0].id, self.articulo.id)

    def test_articulo_repr(self):
        fecha_fija = datetime(2026, 5, 12, 9, 30, 0)
        articulo = Articulo(
            nombre='Router de laboratorio',
            codigo='RED-008',
            id_categoria=self.articulo.id_categoria,
            cantidad=3,
            estado='Disponible',
            nivel_minimo=1,
            fecha_publicacion=fecha_fija
        )
        esperado = f"Articulo('Router de laboratorio', '{fecha_fija}')"
        self.assertEqual(repr(articulo), esperado)


if __name__ == '__main__':
    unittest.main()