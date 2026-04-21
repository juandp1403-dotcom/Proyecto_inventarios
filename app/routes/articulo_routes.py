from flask import Blueprint, jsonify, request
from app.routes.auth_helpers import role_required
from app.models.articulo import Articulo

articulo_bp = Blueprint('articulo', __name__, url_prefix='/articulos')


@articulo_bp.route('/', methods=['GET'])
@role_required('aprendiz', 'instructor', 'auditor', 'revisor')
def listar_articulos():
    return jsonify({'message': 'Listado de artículos en inventario'})


@articulo_bp.route('/<int:articulo_id>', methods=['GET'])
@role_required('aprendiz', 'instructor', 'auditor', 'revisor')
def ver_articulo(articulo_id):
    return jsonify({'message': f'Detalle del artículo {articulo_id}'})


@articulo_bp.route('/', methods=['POST'])
@role_required('auditor', 'revisor')
def crear_articulo():
    data = request.get_json() or {}
    return jsonify({'message': 'Artículo creado', 'datos': data}), 201


@articulo_bp.route('/<int:articulo_id>', methods=['PUT'])
@role_required('auditor', 'revisor')
def editar_articulo(articulo_id):
    data = request.get_json() or {}
    return jsonify({'message': f'Artículo {articulo_id} actualizado', 'datos': data})


@articulo_bp.route('/<int:articulo_id>', methods=['DELETE'])
@role_required('auditor')
def eliminar_articulo(articulo_id):
    return jsonify({'message': f'Artículo {articulo_id} eliminado'})
