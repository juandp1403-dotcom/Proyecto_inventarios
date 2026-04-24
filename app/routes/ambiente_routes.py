from flask import Blueprint, jsonify, render_template, request
from app import db
from app.models.ambiente import Ambiente
from app.routes.auth_helpers import role_required
from app.routes.auth_decorators import login_required

ambiente_bp = Blueprint('ambiente', __name__, url_prefix='/ambientes')


@ambiente_bp.route('/', methods=['GET'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor', 'aprendiz')
def listar_ambientes():
    from app.routes.auth_helpers import get_user_role
    # Obtener ambientes de la base de datos
    ambientes = Ambiente.query.all()
    return render_template('ambiente/list.html', ambientes=ambientes, current_role=get_user_role())


@ambiente_bp.route('/<int:ambiente_id>', methods=['GET'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor', 'aprendiz')
def ver_ambiente(ambiente_id):
    from app.routes.auth_helpers import get_user_role
    # Obtener ambiente específico
    ambiente = Ambiente.query.get_or_404(ambiente_id)
    return render_template('ambiente/detail.html', ambiente=ambiente, current_role=get_user_role())


@ambiente_bp.route('/<int:ambiente_id>/inventario', methods=['GET'])
@login_required
@role_required('admin', 'aprendiz', 'instructor', 'auditor', 'revisor')
def ambiente_inventario(ambiente_id):
    from app.routes.auth_helpers import get_user_role
    ambiente = Ambiente.query.get_or_404(ambiente_id)
    return render_template('inventario/ambiente.html', ambiente=ambiente, current_role=get_user_role())


@ambiente_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'auditor')
def crear_ambiente():
    from app.routes.auth_helpers import get_user_role
    
    if request.method == 'GET':
        return render_template('ambiente/form.html', accion='crear', current_role=get_user_role())
    
    data = request.get_json() or request.form
    ambiente = Ambiente(
        nombre=data.get('nombre'),
        tipo=data.get('tipo'),
        ubicacion=data.get('ubicacion')
    )
    db.session.add(ambiente)
    db.session.commit()
    
    # Generar alerta automática para todos los admin y auditor
    from app.models.alerta import Alerta
    Alerta.crear_alerta(
        titulo='Nuevo Ambiente Creado',
        mensaje=f'Se ha creado el ambiente: {ambiente.nombre}',
        tipo='ambiente'
    )
    
    return jsonify({'message': 'Ambiente creado correctamente', 'id': ambiente.id}), 201


@ambiente_bp.route('/<int:ambiente_id>/editar', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'auditor')
def editar_ambiente(ambiente_id):
    from app.routes.auth_helpers import get_user_role
    ambiente = Ambiente.query.get_or_404(ambiente_id)
    
    if request.method == 'GET':
        return render_template('ambiente/form.html', ambiente=ambiente, accion='editar', current_role=get_user_role())
    
    data = request.get_json() or request.form
    ambiente.nombre = data.get('nombre', ambiente.nombre)
    ambiente.tipo = data.get('tipo', ambiente.tipo)
    ambiente.ubicacion = data.get('ubicacion', ambiente.ubicacion)
    
    db.session.commit()
    
    # Generar alerta automática para todos los admin y auditor
    from app.models.alerta import Alerta
    Alerta.crear_alerta(
        titulo='Ambiente Actualizado',
        mensaje=f'Se ha actualizado el ambiente: {ambiente.nombre}',
        tipo='ambiente'
    )
    
    return jsonify({'message': 'Ambiente actualizado correctamente'})
