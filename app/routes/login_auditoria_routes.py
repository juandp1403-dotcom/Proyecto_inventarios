from flask import Blueprint, jsonify
from app.routes.auth_helpers import role_required
from app.models.login_auditoria import Login_auditoria

login_auditoria_bp = Blueprint('login_auditoria', __name__, url_prefix='/login_auditoria')


@login_auditoria_bp.route('/', methods=['GET'])
@role_required('auditor')
def listar_logins_auditoria():
    return jsonify({'message': 'Listado de logins de auditoría'})
