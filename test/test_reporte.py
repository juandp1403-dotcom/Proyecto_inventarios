import json
import os
import sys
import unittest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import db
from app.models.reporte import Reporte
from test.base_test import BaseTestCase


class TestReporteModel(BaseTestCase):
    """
    Pruebas unitarias para el modelo Reporte (app/models/reporte.py).

    Contexto en la aplicación:
    El modelo Reporte permite almacenar y consultar informes generados en el sistema
    (inventario general, bajas, existencias por ambiente, o auditoría de movimientos).
    Registra el tipo de reporte, los filtros aplicados en formato de texto o JSON, el usuario
    autor (con relación bidireccional 'usuario.reportes') y opcionalmente el ambiente evaluado
    (con relación bidireccional 'ambiente.reportes').
    Además, en 'app/routes/reporte_routes.py' se filtran los reportes según el rol del usuario
    (los instructores/aprendices solo ven sus propios reportes).
    """

    def setUp(self):
        super().setUp()
        self.rol_instructor = self.crear_rol(nombre='instructor', descripcion='Rol docente')
        self.rol_admin = self.crear_rol(nombre='admin', descripcion='Rol administrador')

        self.usuario_docente = self.crear_usuario(
            nombre='profesor_juan',
            email='juan@sena.edu.co',
            rol=self.rol_instructor
        )
        self.usuario_admin = self.crear_usuario(
            nombre='admin_sistema',
            email='admin@sena.edu.co',
            rol=self.rol_admin
        )
        self.ambiente = self.crear_ambiente(
            nombre='Laboratorio IoT',
            tipo='Laboratorio Especializado'
        )

    def test_crear_reporte_general_sin_ambiente(self):
        """Valida la creación de un reporte global sin estar asociado a un ambiente específico."""
        reporte = Reporte(
            tipo='inventario_global',
            filtros='{"categoria": "Todos", "estado": "Activo"}',
            id_usuario=self.usuario_admin.id,
            id_ambiente=None
        )
        db.session.add(reporte)
        db.session.commit()

        self.assertIsNotNone(reporte.id)
        self.assertEqual(reporte.tipo, 'inventario_global')
        self.assertIsNone(reporte.id_ambiente)
        self.assertIsNone(reporte.ambiente)
        self.assertEqual(reporte.usuario.id, self.usuario_admin.id)
        self.assertIsInstance(reporte.fecha_creacion, datetime)

    def test_crear_reporte_con_ambiente_y_relaciones(self):
        """
        Valida que un reporte asociado a un ambiente establezca correctamente
        las relaciones bidireccionales reporte.ambiente y ambiente.reportes.
        """
        reporte = Reporte(
            tipo='inventario_ambiente',
            filtros='{"disponibilidad": "alta"}',
            id_usuario=self.usuario_docente.id,
            id_ambiente=self.ambiente.id
        )
        db.session.add(reporte)
        db.session.commit()

        # Acceso directo al objeto relacionado
        self.assertEqual(reporte.ambiente.nombre, 'Laboratorio IoT')

        # Navegación inversa mediante backref
        self.assertIn(reporte, self.ambiente.reportes)

    def test_relacion_usuario_reportes_backref(self):
        """Valida que un usuario tenga acceso a la lista de reportes que ha generado (usuario.reportes)."""
        r1 = Reporte(tipo='reporte_articulos', id_usuario=self.usuario_docente.id)
        r2 = Reporte(tipo='reporte_solicitudes', id_usuario=self.usuario_docente.id)
        db.session.add_all([r1, r2])
        db.session.commit()

        self.assertEqual(len(self.usuario_docente.reportes), 2)
        self.assertIn(r1, self.usuario_docente.reportes)
        self.assertIn(r2, self.usuario_docente.reportes)

    def test_reporte_campos_obligatorios(self):
        """Valida que tipo e id_usuario no puedan ser nulos."""
        # Sin tipo
        r_sin_tipo = Reporte(tipo=None, id_usuario=self.usuario_admin.id)
        db.session.add(r_sin_tipo)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        # Sin id_usuario
        r_sin_user = Reporte(tipo='general', id_usuario=None)
        db.session.add(r_sin_user)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_almacenamiento_filtros_json(self):
        """Valida que el campo filtros almacene estructuras complejas en formato JSON."""
        filtros_dict = {
            'fecha_desde': '2026-01-01',
            'fecha_hasta': '2026-06-30',
            'estado': 'Disponible',
            'nivel_stock': 'bajo'
        }
        reporte = Reporte(
            tipo='auditoria_stock',
            filtros=json.dumps(filtros_dict),
            id_usuario=self.usuario_admin.id
        )
        db.session.add(reporte)
        db.session.commit()

        recuperado = db.session.get(Reporte, reporte.id)
        filtros_recuperados = json.loads(recuperado.filtros)
        self.assertEqual(filtros_recuperados['estado'], 'Disponible')
        self.assertEqual(filtros_recuperados['nivel_stock'], 'bajo')

    def test_consulta_reportes_por_autor(self):
        """
        Valida la lógica de consulta utilizada en 'reporte_routes.py' para restringir
        la visualización de reportes de instructores o aprendices únicamente a los suyos.
        """
        r_docente = Reporte(tipo='reporte_docente', id_usuario=self.usuario_docente.id)
        r_admin = Reporte(tipo='reporte_admin', id_usuario=self.usuario_admin.id)
        db.session.add_all([r_docente, r_admin])
        db.session.commit()

        reportes_docente = Reporte.query.filter_by(id_usuario=self.usuario_docente.id).all()
        self.assertEqual(len(reportes_docente), 1)
        self.assertEqual(reportes_docente[0].tipo, 'reporte_docente')

    def test_reporte_repr(self):
        """Valida el método __repr__ de Reporte."""
        fecha_fija = datetime(2026, 4, 20, 15, 0, 0)
        reporte = Reporte(
            tipo='bajas_activos',
            filtros='{"anio": 2026}',
            id_usuario=self.usuario_admin.id,
            fecha_creacion=fecha_fija
        )
        esperado = f"Reporte('bajas_activos', '{{\"anio\": 2026}}', '{fecha_fija}')"
        self.assertEqual(repr(reporte), esperado)


if __name__ == '__main__':
    unittest.main()
