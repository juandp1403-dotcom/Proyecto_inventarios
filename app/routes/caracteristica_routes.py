from flask import Blueprint, jsonify, request
from app.routes.auth_helpers import role_required
from app.routes.auth_decorators import login_required
from app.models.caracteristica import Caracteristica

caracteristica_bp = Blueprint('caracteristica', __name__, url_prefix='/caracteristicas')


@caracteristica_bp.route('/', methods=['GET'])
@login_required
@role_required('aprendiz', 'instructor', 'auditor', 'revisor')
def listar_caracteristicas():
    return jsonify({'message': 'Listado de características de artículos'})


@caracteristica_bp.route('/<int:caracteristica_id>', methods=['GET'])
@login_required
@role_required('aprendiz', 'instructor', 'auditor', 'revisor')
def ver_caracteristica(caracteristica_id):
    return jsonify({'message': f'Detalle de característica {caracteristica_id}'})


@caracteristica_bp.route('/', methods=['POST'])
@login_required
@role_required('auditor')
def crear_caracteristica():
    data = request.get_json() or {}
    return jsonify({'message': 'Característica creada', 'datos': data}), 201


@caracteristica_bp.route('/<int:caracteristica_id>', methods=['PUT'])
@login_required
@role_required('auditor')
def editar_caracteristica(caracteristica_id):
    data = request.get_json() or {}
    return jsonify({'message': f'Característica {caracteristica_id} actualizada', 'datos': data})
