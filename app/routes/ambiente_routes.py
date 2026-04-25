from flask import Blueprint, jsonify, render_template, request, session
from app import db
from app.models.ambiente import Ambiente
from app.models.articulo import Articulo
from app.models.inventario_ambiente import InventarioAmbiente
from app.routes.auth_helpers import role_required, get_user_role
from app.routes.auth_decorators import login_required

ambiente_bp = Blueprint('ambiente', __name__, url_prefix='/ambientes')


@ambiente_bp.route('/', methods=['GET'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor', 'aprendiz')
def listar_ambientes():
    ambientes = Ambiente.query.all()
    return render_template('ambiente/list.html', ambientes=ambientes, current_role=get_user_role())


@ambiente_bp.route('/<int:ambiente_id>', methods=['GET'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor', 'aprendiz')
def ver_ambiente(ambiente_id):
    ambiente = Ambiente.query.get_or_404(ambiente_id)
    return render_template('ambiente/detail.html', ambiente=ambiente, current_role=get_user_role())


@ambiente_bp.route('/<int:ambiente_id>/inventario', methods=['GET'])
@login_required
@role_required('admin', 'aprendiz', 'instructor', 'auditor', 'revisor')
def ambiente_inventario(ambiente_id):
    ambiente = Ambiente.query.get_or_404(ambiente_id)
    return render_template('inventario/ambiente.html', ambiente=ambiente, current_role=get_user_role())


@ambiente_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'auditor')
def crear_ambiente():
    if request.method == 'GET':
        return render_template('inventario/crear_ambiente.html', accion='crear', current_role=get_user_role())
    
    data = request.get_json() or request.form
    ambiente = Ambiente(
        nombre=data.get('nombre'),
        tipo=data.get('tipo'),
        ubicacion=data.get('ubicacion')
    )
    db.session.add(ambiente)
    db.session.commit()
    
    items = data.get('items', [])
    for item in items:
        nombre_articulo = item.get('nombre', '').strip()
        cantidad = int(item.get('cantidad', 0))
        cantidad_minima = int(item.get('cantidad_minima', 2))
        
        if not nombre_articulo:
            continue
        
        articulo = Articulo.query.filter_by(nombre=nombre_articulo).first()
        if not articulo:
            articulo = Articulo(
                nombre=nombre_articulo,
                codigo=f'ART-{articulo.id if articulo else 0}',
                descripcion='',
                id_categoria=1,
                cantidad=cantidad,
                nivel_minimo=cantidad_minima,
                estado='disponible'
            )
            db.session.add(articulo)
            db.session.commit()
        
        db.session.add(InventarioAmbiente(
            id_ambiente=ambiente.id,
            id_articulo=articulo.id,
            cantidad=cantidad,
            cantidad_minima=cantidad_minima
        ))
    
    db.session.commit()
    
    return jsonify({'message': 'Ambiente creado correctamente', 'id': ambiente.id}), 201


@ambiente_bp.route('/<int:ambiente_id>/editar', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'auditor')
def editar_ambiente(ambiente_id):
    ambiente = Ambiente.query.get_or_404(ambiente_id)
    
    if request.method == 'GET':
        return render_template('inventario/crear_ambiente.html', ambiente=ambiente, accion='editar', current_role=get_user_role())
    
    data = request.get_json() or request.form
    ambiente.nombre = data.get('nombre', ambiente.nombre)
    ambiente.tipo = data.get('tipo', ambiente.tipo)
    ambiente.ubicacion = data.get('ubicacion', ambiente.ubicacion)
    
    db.session.commit()
    
    return jsonify({'message': 'Ambiente actualizado correctamente'})
