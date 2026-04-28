from flask import Blueprint, jsonify, request, render_template, session
from app import db
from app.routes.auth_helpers import role_required, get_user_role
from app.routes.auth_decorators import login_required
from app.models.ambiente import Ambiente
from app.models.inventario_ambiente import InventarioAmbiente
from app.models.articulo import Articulo
from app.models.alerta import Alerta
from app.models.historial_revision import HistorialRevision

inventario_bp = Blueprint('inventario', __name__, url_prefix='/inventario')


@inventario_bp.route('/', methods=['GET'])
@login_required
def listar_inventarios():
    ambientes = Ambiente.query.all()
    return render_template('inventario/list.html', ambientes=ambientes, current_role=get_user_role())


@inventario_bp.route('/ambiente/<int:ambiente_id>', methods=['GET'])
@login_required
def inventario_por_ambiente(ambiente_id):
    ambiente = Ambiente.query.get_or_404(ambiente_id)
    inventario_items = InventarioAmbiente.query.filter_by(id_ambiente=ambiente_id).all()
    articulos = {a.id: a.nombre for a in Articulo.query.all()}
    return render_template('inventario/ambiente.html', 
                        ambiente=ambiente, 
                        inventario_items=inventario_items,
                        articulos=articulos,
                        current_role=get_user_role())


@inventario_bp.route('/editar/<int:ambiente_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def editar_inventario_amiente(ambiente_id):
    ambiente = Ambiente.query.get_or_404(ambiente_id)
    
    if request.method == 'GET':
        inventario_items = InventarioAmbiente.query.filter_by(id_ambiente=ambiente_id).all()
        items_json = []
        for item in inventario_items:
            articulo = Articulo.query.get(item.id_articulo)
            items_json.append({
                'id': item.id,
                'nombre_articulo': articulo.nombre if articulo else '',
                'cantidad': item.cantidad,
                'cantidad_minima': item.cantidad_minima
            })
        return render_template('inventario/editar_inventario.html',
                              ambiente=ambiente,
                              inventario_items=items_json,
                              current_role=get_user_role())
    
    data = request.get_json() or {}
    items = data.get('items', [])
    
    InventarioAmbiente.query.filter_by(id_ambiente=ambiente_id).delete()
    
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
                codigo='ART-' + str(articulo.id if hasattr(articulo, 'id') else 0),
                descripcion='',
                id_categoria=1,
                cantidad=cantidad,
                nivel_minimo=cantidad_minima,
                estado='disponible'
            )
            db.session.add(articulo)
            db.session.commit()
        
        db.session.add(InventarioAmbiente(
            id_ambiente=ambiente_id,
            id_articulo=articulo.id,
            cantidad=cantidad,
            cantidad_minima=cantidad_minima
        ))
    
    db.session.commit()
    
    HistorialRevision.registrar_revision(
        id_ambiente=ambiente_id,
        tipo_accion='edicion_inventario',
        descripcion=f'Inventario del ambiente actualizado',
        id_usuario=session.get('user_id')
    )
    
    return jsonify({'message': 'Inventario actualizado correctamente'})


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


@inventario_bp.route('/checklist_general/<int:ambiente_id>', methods=['POST'])
@login_required
def checklist_general(ambiente_id):
    from app.models.movimiento import Movimiento
    
    data = request.get_json() or {}
    observaciones = data.get('observaciones', '')
    
    inventario_items = InventarioAmbiente.query.filter_by(id_ambiente=ambiente_id).all()
    
    for inventario in inventario_items:
        movimiento = Movimiento(
            tipo='checklist',
            id_articulo=inventario.id_articulo,
            id_usuario=session.get('user_id'),
            cantidad=inventario.cantidad,
            observacion=observaciones
        )
        db.session.add(movimiento)
    
    db.session.commit()
    
    descripcion = f'Checklist general realizado para ambiente #{ambiente_id}'
    if observaciones:
        descripcion += f' - Observación: {observaciones}'
    
    HistorialRevision.registrar_revision(
        id_ambiente=ambiente_id,
        tipo_accion='checklist',
        descripcion=descripcion,
        id_referencia=ambiente_id,
        id_usuario=session.get('user_id')
    )
    
    return jsonify({'message': 'Checklist general registrado correctamente'})


@inventario_bp.route('/solicitud/<int:inventario_id>', methods=['POST'])
@login_required
@role_required('admin', 'auditor', 'instructor')
def crear_solicitud(inventario_id):
    from app.models.solicitud import Solicitud
    
    inventario = InventarioAmbiente.query.get_or_404(inventario_id)
    data = request.get_json() or {}
    
    solicitud = Solicitud(
        id_usuario=session.get('user_id'),
        id_ambiente=data.get('id_ambiente'),
        cantidad=int(data.get('cantidad', 1)),
        justificacion=data.get('descripcion', ''),
        estado='pendiente'
    )
    db.session.add(solicitud)
    db.session.commit()
    
    HistorialRevision.registrar_revision(
        id_ambiente=inventario.id_ambiente,
        tipo_accion='solicitud',
        descripcion=f'Solicitud #{solicitud.id} creada: {solicitud.justificacion[:50]}',
        id_referencia=solicitud.id,
        id_usuario=session.get('user_id')
    )
    
    Alerta.crear_alerta(
        titulo='Nueva solicitud',
        mensaje=f'Solicitud #{solicitud.id}: {solicitud.justificacion[:50]}',
        tipo='solicitud',
        id_referencia=solicitud.id
    )
    
    return jsonify({'message': 'Solicitud creada correctamente'})


@inventario_bp.route('/reporte/<int:inventario_id>', methods=['POST'])
@login_required
@role_required('admin', 'auditor', 'instructor')
def crear_reporte(inventario_id):
    from app.models.reporte import Reporte
    
    inventario = InventarioAmbiente.query.get_or_404(inventario_id)
    data = request.get_json() or {}
    
    reporte = Reporte(
        tipo='inventario',
        filtros=data.get('descripcion', ''),
        id_usuario=session.get('user_id'),
        id_ambiente=data.get('id_ambiente')
    )
    db.session.add(reporte)
    db.session.commit()
    
    HistorialRevision.registrar_revision(
        id_ambiente=inventario.id_ambiente,
        tipo_accion='reporte',
        descripcion=f'Reporte #{reporte.id} creado: {reporte.filtros[:50]}',
        id_referencia=reporte.id,
        id_usuario=session.get('user_id')
    )
    
    Alerta.crear_alerta(
        titulo='Nuevo reporte',
        mensaje=f'Reporte #{reporte.id}: {reporte.filtros[:50]}',
        tipo='reporte',
        id_referencia=reporte.id
    )
    
    return jsonify({'message': 'Reporte creado correctamente'})


@inventario_bp.route('/actualizar/<int:inventario_id>', methods=['POST'])
@login_required
@role_required('admin', 'auditor', 'instructor')
def actualizar_inventario(inventario_id):
    inventario = InventarioAmbiente.query.get_or_404(inventario_id)
    data = request.get_json() or {}
    
    if data.get('cantidad'):
        inventario.cantidad = int(data.get('cantidad'))
    if data.get('cantidad_minima'):
        inventario.cantidad_minima = int(data.get('cantidad_minima'))
    
    db.session.commit()
    
    HistorialRevision.registrar_revision(
        id_ambiente=inventario.id_ambiente,
        tipo_accion='actualizacion',
        descripcion=f'Inventario #{inventario_id} actualizado',
        id_referencia=inventario_id,
        id_usuario=session.get('user_id')
    )
    
    return jsonify({'message': 'Inventario actualizado correctamente'})


@inventario_bp.route('/eliminar_todo/<int:ambiente_id>', methods=['POST'])
@login_required
@role_required('admin')
def eliminar_todo_inventario(ambiente_id):
    InventarioAmbiente.query.filter_by(id_ambiente=ambiente_id).delete()
    db.session.commit()
    
    return jsonify({'message': 'Inventario eliminado correctamente'})
