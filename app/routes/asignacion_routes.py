from flask import Blueprint, jsonify, request
from app.routes.auth_helpers import role_required
from app.models.asignacion import Asignacion

asignacion_bp = Blueprint('asignacion', __name__, url_prefix='/asignaciones')


@asignacion_bp.route('/', methods=['GET'])
@role_required('instructor', 'auditor', 'revisor')
def listar_asignaciones():
    return jsonify({'message': 'Listado de asignaciones de artículos'})


@asignacion_bp.route('/', methods=['POST'])
@role_required('auditor', 'revisor')
def crear_asignacion():
    data = request.get_json() or {}
    return jsonify({'message': 'Asignación creada', 'datos': data}), 201
