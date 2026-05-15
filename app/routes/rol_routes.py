from flask import Blueprint, jsonify
from app.routes.auth_helpers import role_required
from app.routes.auth_decorators import login_required
from app.models.rol import Rol

rol_bp = Blueprint('rol', __name__, url_prefix='/roles')


@rol_bp.route('/', methods=['GET'])
@login_required
@role_required('auditor', 'revisor')
def listar_roles():
    return jsonify({'message': 'Listado de roles disponibles'})


@rol_bp.route('/', methods=['POST'])
@login_required
@role_required('auditor')
def crear_rol():
    return jsonify({'message': 'Rol creado'})
