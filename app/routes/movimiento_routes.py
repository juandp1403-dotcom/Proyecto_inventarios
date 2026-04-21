from flask import Blueprint, jsonify, request
from app.routes.auth_helpers import role_required
from app.models.movimiento import Movimiento

movimiento_bp = Blueprint('movimiento', __name__, url_prefix='/movimientos')


@movimiento_bp.route('/', methods=['GET'])
@role_required('auditor', 'revisor')
def listar_movimientos():
    return jsonify({'message': 'Listado de movimientos de inventario'})


@movimiento_bp.route('/', methods=['POST'])
@role_required('auditor', 'revisor')
def crear_movimiento():
    data = request.get_json() or {}
    return jsonify({'message': 'Movimiento creado', 'datos': data}), 201
