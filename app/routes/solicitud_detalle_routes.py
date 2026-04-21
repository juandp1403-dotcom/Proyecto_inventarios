from flask import Blueprint, jsonify, request
from app.routes.auth_helpers import role_required
from app.models.solicitud_detalle import SolicitudDetalle

solicitud_detalle_bp = Blueprint('solicitud_detalle', __name__, url_prefix='/solicitud_detalles')


@solicitud_detalle_bp.route('/', methods=['GET'])
@role_required('revisor', 'auditor')
def listar_detalles():
    return jsonify({'message': 'Listado de detalles de solicitud'})


@solicitud_detalle_bp.route('/', methods=['POST'])
@role_required('revisor')
def crear_detalle():
    data = request.get_json() or {}
    return jsonify({'message': 'Detalle de solicitud creado', 'datos': data}), 201
