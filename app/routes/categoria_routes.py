from flask import Blueprint, jsonify, request
from app.routes.auth_helpers import role_required
from app.models.categoria import Categoria

categoria_bp = Blueprint('categoria', __name__, url_prefix='/categorias')


@categoria_bp.route('/', methods=['GET'])
@role_required('aprendiz', 'instructor', 'auditor', 'revisor')
def listar_categorias():
    return jsonify({'message': 'Listado de categorías de artículos'})


@categoria_bp.route('/<int:categoria_id>', methods=['GET'])
@role_required('aprendiz', 'instructor', 'auditor', 'revisor')
def ver_categoria(categoria_id):
    return jsonify({'message': f'Detalle de categoría {categoria_id}'})


@categoria_bp.route('/', methods=['POST'])
@role_required('auditor')
def crear_categoria():
    data = request.get_json() or {}
    return jsonify({'message': 'Categoría creada', 'datos': data}), 201


@categoria_bp.route('/<int:categoria_id>', methods=['PUT'])
@role_required('auditor')
def editar_categoria(categoria_id):
    data = request.get_json() or {}
    return jsonify({'message': f'Categoría {categoria_id} actualizada', 'datos': data})
