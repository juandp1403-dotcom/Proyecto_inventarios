from flask import Blueprint, jsonify, request, render_template
from app.routes.auth_helpers import role_required
from app.routes.auth_decorators import login_required
from app.models.reporte import Reporte

reporte_bp = Blueprint('reporte', __name__, url_prefix='/reportes')


@reporte_bp.route('/', methods=['GET'])
@login_required
@role_required('admin', 'auditor', 'revisor')
def listar_reportes():
    from app.routes.auth_helpers import get_user_role
    # Obtener reportes de la base de datos
    reportes = Reporte.query.all()
    return render_template('reporte/list.html', reportes=reportes, current_role=get_user_role())


@reporte_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'auditor', 'revisor')
def crear_reporte():
    from app.routes.auth_helpers import get_user_role
    if request.method == 'GET':
        return render_template('reporte/form.html', accion='crear', current_role=get_user_role())
    
    data = request.get_json() or request.form
    reporte = Reporte(
        tipo=data.get('tipo'),
        filtros=data.get('filtros'),
        id_usuario=session.get('user_id')
    )
    db.session.add(reporte)
    db.session.commit()
    
    # Generar alerta automática para todos los admin y auditor
    from app.models.alerta import Alerta
    Alerta.crear_alerta(
        titulo='Nuevo Reporte Generado',
        mensaje=f'Se ha generado un nuevo reporte: {data.get("tipo")}',
        tipo='reporte'
    )
    
    return jsonify({'message': 'Reporte creado correctamente', 'id': reporte.id}), 201


@reporte_bp.route('/', methods=['POST'])
@role_required('instructor', 'auditor', 'revisor')
def crear_reporte_api():
    data = request.get_json() or {}
    return jsonify({'message': 'Reporte generado', 'datos': data}), 201
