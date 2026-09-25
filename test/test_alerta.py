import os
import sys
import unittest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import db
from app.models.alerta import Alerta
from test.base_test import BaseTestCase


class TestAlertaModel(BaseTestCase):
    """Pruebas unitarias para el modelo Alerta."""

    def setUp(self):
        super().setUp()
        rol_usuario = self.crear_rol(nombre='usuario')
        self.usuario = self.crear_usuario(
            nombre='usuario_alertas',
            email='alertas@sena.edu.co',
            rol=rol_usuario
        )

    def test_crear_alerta_y_valores_por_defecto(self):
        alerta = Alerta(
            titulo='Stock bajo',
            mensaje='Quedan pocas unidades del artículo',
            tipo='inventario',
            id_usuario_destino=self.usuario.id,
            id_referencia=12
        )
        db.session.add(alerta)
        db.session.commit()

        guardada = db.session.get(Alerta, alerta.id)
        self.assertIsNotNone(guardada)
        self.assertEqual(guardada.titulo, 'Stock bajo')
        self.assertEqual(guardada.mensaje, 'Quedan pocas unidades del artículo')
        self.assertEqual(guardada.tipo, 'inventario')
        self.assertEqual(guardada.id_usuario_destino, self.usuario.id)
        self.assertEqual(guardada.id_referencia, 12)
        self.assertFalse(guardada.leida)
        self.assertIsInstance(guardada.fecha_creacion, datetime)

    def test_crear_alerta_para_usuario(self):
        alerta = Alerta.crear_alerta(
            titulo='Solicitud aprobada',
            mensaje='La solicitud fue aprobada',
            tipo='solicitud',
            id_usuario_destino=self.usuario.id
        )

        self.assertIsNotNone(alerta.id)
        self.assertEqual(alerta.id_usuario_destino, self.usuario.id)
        self.assertEqual(Alerta.query.count(), 1)

    def test_crear_alertas_para_roles_destino(self):
        usuarios = []
        for nombre_rol in ('admin', 'auditor', 'revisor'):
            rol = self.crear_rol(nombre=nombre_rol)
            usuarios.append(self.crear_usuario(
                nombre=f'usuario_{nombre_rol}',
                email=f'{nombre_rol}@sena.edu.co',
                rol=rol
            ))

        resultado = Alerta.crear_alerta(
            titulo='Revisión requerida',
            mensaje='Hay elementos pendientes de revisión',
            tipo='reporte',
            id_referencia=7
        )

        self.assertIsNone(resultado)
        alertas = Alerta.query.filter_by(titulo='Revisión requerida').all()
        self.assertEqual(len(alertas), 3)
        self.assertEqual(
            {alerta.id_usuario_destino for alerta in alertas},
            {usuario.id for usuario in usuarios}
        )

    def test_alerta_campos_obligatorios(self):
        alerta = Alerta(
            titulo=None,
            mensaje='Mensaje',
            tipo='inventario',
            id_usuario_destino=self.usuario.id
        )
        db.session.add(alerta)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_alerta_repr(self):
        alerta = Alerta(
            titulo='Equipo pendiente',
            mensaje='Revisar equipo',
            tipo='ambiente',
            id_usuario_destino=self.usuario.id
        )
        self.assertEqual(repr(alerta), "Alerta('Equipo pendiente')")


if __name__ == '__main__':
    unittest.main()