from flask import Blueprint, jsonify, request
from app.routes.auth_helpers import role_required
from app.routes.auth_decorators import login_required
from app.models.articulo_caracteristica import Articulo_caracteristica

articulo_caracteristica_bp = Blueprint('articulo_caracteristica', __name__, url_prefix='/articulo_caracteristicas')


@articulo_caracteristica_bp.route('/', methods=['GET'])
@login_required
@role_required('aprendiz', 'instructor', 'auditor', 'revisor')
def listar_relaciones():
    return jsonify({'message': 'Listado de relaciones artículo/característica'})


@articulo_caracteristica_bp.route('/', methods=['POST'])
@login_required
@role_required('auditor', 'revisor')
def crear_relacion():
    data = request.get_json() or {}
    return jsonify({'message': 'Relación creada', 'datos': data}), 201


@articulo_caracteristica_bp.route('/<int:relacion_id>', methods=['DELETE'])
@login_required
@role_required('auditor')
def eliminar_relacion(relacion_id):
    return jsonify({'message': f'Relación {relacion_id} eliminada'})
