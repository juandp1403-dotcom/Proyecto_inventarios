import os
import sys
import unittest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import db
from app.models.movimiento import Movimiento
from test.base_test import BaseTestCase


class TestMovimientoModel(BaseTestCase):
    """
    Pruebas unitarias para el modelo Movimiento (app/models/movimiento.py).

    Contexto en la aplicación:
    El modelo Movimiento registra la trazabilidad transaccional (Kárdex) de los artículos del inventario.
    Cada vez que se abastece material o se entrega a instructores/aprendices, se crea un registro
    indicando el tipo ('entrada' o 'salida'), la cantidad modificada, el artículo afectado,
    el usuario responsable (auditor o revisor según app/routes/movimiento_routes.py) y una observación.
    """

    def setUp(self):
        super().setUp()
        self.rol_auditor = self.crear_rol(nombre='auditor', descripcion='Rol auditor')
        self.usuario_auditor = self.crear_usuario(
            nombre='auditor_inv',
            email='auditor.inv@sena.edu.co',
            rol=self.rol_auditor
        )
        self.articulo = self.crear_articulo(
            nombre='Osciloscopio Digital',
            codigo='ELEC-005',
            cantidad=10
        )

    def test_crear_movimiento_entrada_exitoso(self):
        """Valida el registro de una entrada de inventario por dotación o compra."""
        movimiento = Movimiento(
            id_articulo=self.articulo.id,
            id_usuario=self.usuario_auditor.id,
            tipo='entrada',
            cantidad=5,
            observacion='Recepción de dotación institucional'
        )
        db.session.add(movimiento)
        db.session.commit()

        self.assertIsNotNone(movimiento.id)
        self.assertEqual(movimiento.id_articulo, self.articulo.id)
        self.assertEqual(movimiento.id_usuario, self.usuario_auditor.id)
        self.assertEqual(movimiento.tipo, 'entrada')
        self.assertEqual(movimiento.cantidad, 5)
        self.assertEqual(movimiento.observacion, 'Recepción de dotación institucional')
        self.assertIsInstance(movimiento.fecha_movimiento, datetime)

    def test_crear_movimiento_salida_exitoso(self):
        """Valida el registro de una salida de inventario para uso en formación técnica."""
        movimiento = Movimiento(
            id_articulo=self.articulo.id,
            id_usuario=self.usuario_auditor.id,
            tipo='salida',
            cantidad=2,
            observacion='Entrega para práctica de laboratorio'
        )
        db.session.add(movimiento)
        db.session.commit()

        guardado = db.session.get(Movimiento, movimiento.id)
        self.assertIsNotNone(guardado)
        self.assertEqual(guardado.tipo, 'salida')
        self.assertEqual(guardado.cantidad, 2)

    def test_movimiento_campos_obligatorios(self):
        """Valida que id_articulo, id_usuario, tipo y cantidad sean obligatorios."""
        # Sin id_articulo
        m1 = Movimiento(id_articulo=None, id_usuario=self.usuario_auditor.id, tipo='entrada', cantidad=1)
        db.session.add(m1)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        # Sin id_usuario
        m2 = Movimiento(id_articulo=self.articulo.id, id_usuario=None, tipo='entrada', cantidad=1)
        db.session.add(m2)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        # Sin tipo
        m3 = Movimiento(id_articulo=self.articulo.id, id_usuario=self.usuario_auditor.id, tipo=None, cantidad=1)
        db.session.add(m3)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        # Sin cantidad
        m4 = Movimiento(id_articulo=self.articulo.id, id_usuario=self.usuario_auditor.id, tipo='entrada', cantidad=None)
        db.session.add(m4)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_movimiento_observacion_opcional(self):
        """Valida que la observación sea opcional (nullable=True)."""
        movimiento = Movimiento(
            id_articulo=self.articulo.id,
            id_usuario=self.usuario_auditor.id,
            tipo='entrada',
            cantidad=3,
            observacion=None
        )
        db.session.add(movimiento)
        db.session.commit()

        guardado = db.session.get(Movimiento, movimiento.id)
        self.assertIsNotNone(guardado)
        self.assertIsNone(guardado.observacion)

    def test_trazabilidad_kardex_movimientos_por_articulo(self):
        """
        Valida que se pueda reconstruir el historial de movimientos de un artículo
        para auditar el flujo neto de existencias (entradas vs salidas).
        """
        mov_entrada = Movimiento(
            id_articulo=self.articulo.id,
            id_usuario=self.usuario_auditor.id,
            tipo='entrada',
            cantidad=10,
            observacion='Ingreso inicial'
        )
        mov_salida = Movimiento(
            id_articulo=self.articulo.id,
            id_usuario=self.usuario_auditor.id,
            tipo='salida',
            cantidad=4,
            observacion='Préstamo a ambiente'
        )
        db.session.add_all([mov_entrada, mov_salida])
        db.session.commit()

        movimientos = Movimiento.query.filter_by(id_articulo=self.articulo.id).order_by(Movimiento.id).all()
        self.assertEqual(len(movimientos), 2)

        total_entradas = sum(m.cantidad for m in movimientos if m.tipo == 'entrada')
        total_salidas = sum(m.cantidad for m in movimientos if m.tipo == 'salida')
        balance_neto = total_entradas - total_salidas

        self.assertEqual(total_entradas, 10)
        self.assertEqual(total_salidas, 4)
        self.assertEqual(balance_neto, 6)

    def test_movimiento_repr(self):
        """Valida el método __repr__ de Movimiento."""
        fecha_fija = datetime(2026, 3, 10, 8, 0, 0)
        movimiento = Movimiento(
            id_articulo=self.articulo.id,
            id_usuario=self.usuario_auditor.id,
            tipo='entrada',
            cantidad=8,
            observacion='Ingreso lote #1',
            fecha_movimiento=fecha_fija
        )
        esperado = f"Movimiento('entrada', '8', '{fecha_fija}', 'Ingreso lote #1')"
        self.assertEqual(repr(movimiento), esperado)


if __name__ == '__main__':
    unittest.main()
