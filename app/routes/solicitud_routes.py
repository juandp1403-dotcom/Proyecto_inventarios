from flask import Blueprint, jsonify, request, render_template, session
from app import db
from app.routes.auth_helpers import role_required, get_user_role
from app.routes.auth_decorators import login_required
from app.models.solicitud import Solicitud
from app.models.usuario import Usuario
from app.models.alerta import Alerta
from app.models.ambiente import Ambiente

solicitud_bp = Blueprint('solicitud', __name__, url_prefix='/solicitudes')


@solicitud_bp.route('/', methods=['GET'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor')
def listar_solicitudes():
    from app.routes.auth_helpers import get_user_role
    role = get_user_role()
    if role == 'instructor':
        solicitudes = Solicitud.query.join(Ambiente).filter(Solicitud.id_usuario == session.get('user_id')).all()
    else:
        solicitudes = Solicitud.query.join(Ambiente).all()
    return render_template('solicitud/list.html', solicitudes=solicitudes, current_role=role)


@solicitud_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor')
def crear_solicitud():
    from app.routes.auth_helpers import get_user_role
    ambientes = Ambiente.query.all()
    if request.method == 'GET':
        return render_template('solicitud/form.html', accion='crear', current_role=get_user_role(), ambientes=ambientes)
    
    data = request.get_json() or request.form
    solicitud = Solicitud(
        justificacion=data.get('justificacion'),
        id_usuario=session.get('user_id'),
        id_ambiente=data.get('id_ambiente'),
        cantidad=int(data.get('cantidad', 1)),
        estado='pendiente'
    )
    db.session.add(solicitud)
    db.session.commit()
    
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
    solicitud = Solicitud.query.get_or_404(solicitud_id)
    solicitud.estado = 'aprobada'
    db.session.commit()
    
    Alerta.crear_alerta(
        titulo='Solicitud aprobada',
        mensaje=f'Tu solicitud #{solicitud_id} ha sido aprobada.',
        tipo='solicitud',
        id_usuario_destino=solicitud.id_usuario,
        id_referencia=solicitud_id
    )
    return jsonify({'message': 'Solicitud aprobada'})


@solicitud_bp.route('/<int:solicitud_id>/rechazar', methods=['POST'])
@login_required
@role_required('admin', 'auditor')
def rechazar_solicitud(solicitud_id):
    solicitud = Solicitud.query.get_or_404(solicitud_id)
    solicitud.estado = 'rechazada'
    db.session.commit()
    
    Alerta.crear_alerta(
        titulo='Solicitud rechazada',
        mensaje=f'Tu solicitud #{solicitud_id} ha sido rechazada.',
        tipo='solicitud',
        id_usuario_destino=solicitud.id_usuario,
        id_referencia=solicitud_id
    )
    return jsonify({'message': 'Solicitud rechazada'})
