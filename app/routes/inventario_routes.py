from flask import Blueprint, jsonify, request, render_template
from app.routes.auth_helpers import role_required, get_user_role
from app.routes.auth_decorators import login_required
from app.models.ambiente import Ambiente

inventario_bp = Blueprint('inventario', __name__, url_prefix='/inventario')


@inventario_bp.route('/', methods=['GET'])
@login_required
@role_required('aprendiz', 'instructor', 'auditor', 'revisor')
def listar_inventarios():
    # Obtener todos los ambientes para mostrar inventario general
    ambientes = Ambiente.query.all()
    return render_template('inventario/list.html', ambientes=ambientes)


@inventario_bp.route('/ambiente/<int:ambiente_id>', methods=['GET'])
@login_required
@role_required('aprendiz', 'instructor', 'auditor', 'revisor')
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
                         inventario_items=inventario_items)


@inventario_bp.route('/articulo/<int:articulo_id>', methods=['GET'])
@role_required('aprendiz', 'instructor', 'auditor', 'revisor')
def detalle_articulo(articulo_id):
    return jsonify({'message': f'Detalle del artículo {articulo_id}'})


@inventario_bp.route('/articulo/<int:articulo_id>', methods=['PUT'])
@role_required('auditor', 'revisor')
def actualizar_articulo(articulo_id):
    data = request.get_json() or {}
    return jsonify({'message': f'Artículo {articulo_id} actualizado', 'datos': data})


@inventario_bp.route('/movimiento', methods=['POST'])
@role_required('auditor', 'revisor')
def movimiento_inventario():
    data = request.get_json() or {}
    return jsonify({'message': 'Movimiento de inventario registrado', 'datos': data})
