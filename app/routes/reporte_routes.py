from flask import Blueprint, jsonify, request, render_template, session
from app import db
from app.routes.auth_helpers import role_required, get_user_role
from app.routes.auth_decorators import login_required
from app.models.reporte import Reporte
from app.models.alerta import Alerta
from app.models.ambiente import Ambiente

reporte_bp = Blueprint('reporte', __name__, url_prefix='/reportes')


@reporte_bp.route('/', methods=['GET'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor')
def listar_reportes():
    from app.routes.auth_helpers import get_user_role
    role = get_user_role()
    if role == 'instructor':
        reportes = Reporte.query.join(Ambiente).filter(Reporte.id_usuario == session.get('user_id')).all()
    else:
        reportes = Reporte.query.join(Ambiente).all()
    return render_template('reporte/list.html', reportes=reportes, current_role=role)


@reporte_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor')
def crear_reporte():
    ambientes = Ambiente.query.all()
    if request.method == 'GET':
        return render_template('reporte/form.html', accion='crear', current_role=get_user_role(), ambientes=ambientes)
    
    data = request.get_json() or request.form
    reporte = Reporte(
        tipo=data.get('tipo'),
        filtros=data.get('filtros'),
        id_usuario=session.get('user_id'),
        id_ambiente=data.get('id_ambiente')
    )
    db.session.add(reporte)
    db.session.commit()
    
    Alerta.crear_alerta(
        titulo='Nuevo reporte',
        mensaje=f'Se ha creado un reporte de tipo: {reporte.tipo}',
        tipo='reporte',
        id_referencia=reporte.id
    )
    
    return jsonify({'message': 'Reporte creado correctamente', 'id': reporte.id}), 201


@reporte_bp.route('/', methods=['POST'])
@login_required
@role_required('instructor', 'auditor', 'revisor')
def crear_reporte_api():
    data = request.get_json() or {}
    return jsonify({'message': 'Reporte generado', 'datos': data}), 201
