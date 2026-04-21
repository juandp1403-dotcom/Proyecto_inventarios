from flask import Blueprint, jsonify, request, render_template
from app.routes.auth_helpers import role_required
from app.routes.auth_decorators import login_required
from app.models.solicitud import Solicitud

solicitud_bp = Blueprint('solicitud', __name__, url_prefix='/solicitudes')


@solicitud_bp.route('/', methods=['GET'])
@role_required('revisor', 'auditor')
def listar_solicitudes():
    # Obtener solicitudes de la base de datos
    solicitudes = Solicitud.query.all()
    return render_template('solicitud/list.html', solicitudes=solicitudes)


@solicitud_bp.route('/crear', methods=['GET', 'POST'])
@role_required('revisor', 'instructor')
def crear_solicitud():
    if request.method == 'GET':
        return render_template('solicitud/form.html', accion='crear')
    
    data = request.get_json() or request.form
    solicitud = Solicitud(
        justificacion=data.get('justificacion'),
        id_usuario=session.get('user_id'),
        estado='pendiente'
    )
    db.session.add(solicitud)
    db.session.commit()
    
    # Generar alerta automática para admin y auditor
    from app.routes.auth_helpers import get_user_role
    current_role = get_user_role()
    if current_role in ['admin', 'auditor']:
        from app.models.alerta import Alerta
        Alerta.crear_alerta(
            titulo='Nueva Solicitud Creada',
            mensaje=f'Se ha creado una nueva solicitud: {data.get("justificacion")}',
            tipo='solicitud',
            id_usuario_destino=session.get('user_id')
        )
    
    return jsonify({'message': 'Solicitud creada correctamente', 'id': solicitud.id}), 201


@solicitud_bp.route('/', methods=['POST'])
@login_required
@role_required('revisor')
def crear_solicitud_api():
    data = request.get_json() or {}
    return jsonify({'message': 'Solicitud creada', 'datos': data}), 201


@solicitud_bp.route('/<int:solicitud_id>/aprobar', methods=['POST'])
@login_required
@role_required('auditor')
def aprobar_solicitud(solicitud_id):
    return jsonify({'message': f'Solicitud {solicitud_id} aprobada'})
