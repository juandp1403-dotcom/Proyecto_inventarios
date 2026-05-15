from flask import Blueprint, jsonify, request
from app.routes.auth_helpers import role_required
from app.routes.auth_decorators import login_required
from app.models.articulo import Articulo

articulo_bp = Blueprint('articulo', __name__, url_prefix='/articulos')


@articulo_bp.route('/', methods=['GET'])
@login_required
@role_required('aprendiz', 'instructor', 'auditor', 'revisor')
def listar_articulos():
    return jsonify({'message': 'Listado de artículos en inventario'})


@articulo_bp.route('/<int:articulo_id>', methods=['GET'])
@login_required
@role_required('aprendiz', 'instructor', 'auditor', 'revisor')
def ver_articulo(articulo_id):
    return jsonify({'message': f'Detalle del artículo {articulo_id}'})


@articulo_bp.route('/', methods=['POST'])
@login_required
@role_required('admin', 'auditor')
def crear_articulo():
    data = request.get_json() or {}
    return jsonify({'message': 'Artículo creado', 'datos': data}), 201


@articulo_bp.route('/<int:articulo_id>', methods=['PUT'])
@login_required
@role_required('admin', 'auditor')
def editar_articulo(articulo_id):
    data = request.get_json() or {}
    return jsonify({'message': f'Artículo {articulo_id} actualizado', 'datos': data})


@articulo_bp.route('/<int:articulo_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def eliminar_articulo(articulo_id):
    return jsonify({'message': f'Artículo {articulo_id} eliminado'})
