from flask import Blueprint, jsonify, request
from app.routes.auth_helpers import role_required
from app.models.reporte_daño import Reporte_daño

reporte_dano_bp = Blueprint('reporte_dano', __name__, url_prefix='/reportes_dano')


@reporte_dano_bp.route('/', methods=['GET'])
@role_required('instructor', 'auditor', 'revisor')
def listar_reportes_dano():
    return jsonify({'message': 'Listado de reportes de daño'})


@reporte_dano_bp.route('/', methods=['POST'])
@role_required('instructor', 'auditor', 'revisor')
def crear_reporte_dano():
    data = request.get_json() or {}
    return jsonify({'message': 'Reporte de daño creado', 'datos': data}), 201
