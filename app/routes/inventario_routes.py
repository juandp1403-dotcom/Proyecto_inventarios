from flask import Blueprint, jsonify, request, render_template, session
from app import db
from app.routes.auth_helpers import role_required, get_user_role
from app.routes.auth_decorators import login_required
from app.models.ambiente import Ambiente

inventario_bp = Blueprint('inventario', __name__, url_prefix='/inventario')


@inventario_bp.route('/', methods=['GET'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor', 'aprendiz')
def listar_inventarios():
    from app.routes.auth_helpers import get_user_role
    # Obtener todos los ambientes para mostrar inventario general
    ambientes = Ambiente.query.all()
    return render_template('inventario/list.html', ambientes=ambientes, current_role=get_user_role())


@inventario_bp.route('/ambiente/<int:ambiente_id>', methods=['GET'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor', 'aprendiz')
def inventario_por_ambiente(ambiente_id):
    ambiente = Ambiente.query.get_or_404(ambiente_id)
    
    # Obtener items del inventario para este ambiente
    from app.models.inventario import Inventario
    from app.models.articulo import Articulo
    
    inventario_items = db.session.query(Inventario, Articulo).join(
        Articulo, Inventario.id_articulo == Articulo.id
    ).filter(
        Inventario.id_ambiente == ambiente_id
    ).all()
    
    return render_template('inventario/ambiente.html', 
                         ambiente=ambiente, 
                         inventario_items=inventario_items,
                         current_role=get_user_role())


@inventario_bp.route('/articulo/<int:articulo_id>', methods=['GET'])
@login_required
@role_required('admin', 'aprendiz', 'instructor', 'auditor', 'revisor')
def detalle_articulo(articulo_id):
    return jsonify({'message': f'Detalle del artículo {articulo_id}'})


@inventario_bp.route('/articulo/<int:articulo_id>', methods=['PUT'])
@login_required
@role_required('auditor', 'revisor')
def actualizar_articulo(articulo_id):
    data = request.get_json() or {}
    return jsonify({'message': f'Artículo {articulo_id} actualizado', 'datos': data})


@inventario_bp.route('/movimiento', methods=['POST'])
@login_required
@role_required('auditor', 'revisor')
def movimiento_inventario():
    data = request.get_json() or {}
    return jsonify({'message': 'Movimiento de inventario registrado', 'datos': data})


@inventario_bp.route('/checklist/<int:inventario_id>', methods=['POST'])
@login_required
@role_required('admin', 'auditor', 'instructor', 'aprendiz')
def checklist_item(inventario_id):
    from app.models.movimiento import Movimiento
    from app.models.inventario import Inventario
    
    inventario = Inventario.query.get_or_404(inventario_id)
    data = request.get_json() or request.form
    
    # Registrar movimiento de checklist
    movimiento = Movimiento(
        tipo='checklist',
        id_articulo=inventario.id_articulo,
        id_usuario=session.get('user_id'),
        cantidad=inventario.cantidad,
        observaciones=f'Checklist realizado: {data.get("observaciones", "")}'
    )
    db.session.add(movimiento)
    db.session.commit()
    
    return jsonify({'message': 'Checklist registrado correctamente'})
