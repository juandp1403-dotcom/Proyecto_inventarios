from flask import Blueprint, jsonify, request, render_template
from app.routes.auth_helpers import role_required
from app.routes.auth_decorators import login_required
from app.models.solicitud import Solicitud

solicitud_bp = Blueprint('solicitud', __name__, url_prefix='/solicitudes')


@solicitud_bp.route('/', methods=['GET'])
@login_required
@role_required('admin', 'auditor', 'revisor')
def listar_solicitudes():
    from app.routes.auth_helpers import get_user_role
    # Obtener solicitudes de la base de datos
    solicitudes = Solicitud.query.all()
    return render_template('solicitud/list.html', solicitudes=solicitudes, current_role=get_user_role())


@solicitud_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor')
def crear_solicitud():
    from app.routes.auth_helpers import get_user_role
    if request.method == 'GET':
        return render_template('solicitud/form.html', accion='crear', current_role=get_user_role())
    
    data = request.get_json() or request.form
    solicitud = Solicitud(
        justificacion=data.get('justificacion'),
        id_usuario=session.get('user_id'),
        estado='pendiente'
    )
    db.session.add(solicitud)
    db.session.commit()
    
    # Generar alerta automática para todos los admin y auditor
    from app.models.alerta import Alerta
    Alerta.crear_alerta(
        titulo='Nueva Solicitud Creada',
        mensaje=f'Se ha creado una nueva solicitud: {data.get("justificacion")}',
        tipo='solicitud'
    )
    
    return jsonify({'message': 'Solicitud creada correctamente', 'id': solicitud.id}), 201


@solicitud_bp.route('/', methods=['POST'])
@login_required
@role_required('admin', 'auditor', 'revisor')
def crear_solicitud_api():
    data = request.get_json() or {}
    return jsonify({'message': 'Solicitud creada', 'datos': data}), 201


@solicitud_bp.route('/<int:solicitud_id>/aprobar', methods=['POST'])
@login_required
@role_required('admin', 'auditor')
def aprobar_solicitud(solicitud_id):
    return jsonify({'message': f'Solicitud {solicitud_id} aprobada'})
