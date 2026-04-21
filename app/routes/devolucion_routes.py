from flask import Blueprint, jsonify, request
from app.routes.auth_helpers import role_required
from app.models.devolucion import Devolucion

devolucion_bp = Blueprint('devolucion', __name__, url_prefix='/devoluciones')


@devolucion_bp.route('/', methods=['GET'])
@role_required('revisor', 'auditor')
def listar_devoluciones():
    return jsonify({'message': 'Listado de devoluciones'})


@devolucion_bp.route('/', methods=['POST'])
@role_required('revisor')
def crear_devolucion():
    data = request.get_json() or {}
    return jsonify({'message': 'Devolución registrada', 'datos': data}), 201
