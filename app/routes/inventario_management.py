from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.routes.auth_helpers import role_required, get_user_role
from app.routes.auth_decorators import login_required
from app.models.inventario import Inventario
from app.models.articulo import Articulo
from app.models.ambiente import Ambiente
from app import db
from flask import session

inventario_management_bp = Blueprint('inventario_management', __name__, url_prefix='/inventario')

@inventario_management_bp.route('/agregar/<int:ambiente_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'auditor')
def agregar_item_ambiente(ambiente_id):
    ambiente = Ambiente.query.get_or_404(ambiente_id)
    
    if request.method == 'GET':
        # Obtener todos los artículos disponibles
        articulos = Articulo.query.all()
        return render_template('inventario/agregar.html', 
                             ambiente=ambiente, 
                             articulos=articulos)
    
    data = request.get_json() or request.form
    articulo_id = data.get('id_articulo')
    cantidad = data.get('cantidad')
    cantidad_minima = data.get('cantidad_minima', 2)
    
    if not articulo_id or not cantidad:
        return jsonify({'error': 'Artículo y cantidad son requeridos'}), 400
    
    # Verificar si ya existe este artículo en el inventario del ambiente
    existencia = Inventario.query.filter_by(
        id_ambiente=ambiente_id,
        id_articulo=articulo_id
    ).first()
    
    if existencia:
        # Actualizar cantidad existente
        existencia.cantidad = cantidad
        existencia.cantidad_minima = cantidad_minima
        mensaje = f'Artículo actualizado en {ambiente.nombre}: {cantidad} unidades'
    else:
        # Crear nuevo registro
        nuevo_inventario = Inventario(
            id_ambiente=ambiente_id,
            id_articulo=articulo_id,
            cantidad=cantidad,
            cantidad_minima=cantidad_minima
        )
        db.session.add(nuevo_inventario)
        mensaje = f'Artículo agregado a {ambiente.nombre}: {cantidad} unidades'
    
    db.session.commit()
    
    # Generar alerta automática
    from app.models.alerta import Alerta
    Alerta.crear_alerta(
        titulo='Inventario Actualizado',
        mensaje=mensaje,
        tipo='inventario',
        id_usuario_destino=session.get('user_id')
    )
    
    return jsonify({'message': 'Item agregado/actualizado correctamente'})

@inventario_management_bp.route('/editar/<int:inventario_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'auditor')
def editar_item_inventario(inventario_id):
    inventario = Inventario.query.get_or_404(inventario_id)
    
    if request.method == 'GET':
        return render_template('inventario/editar.html', inventario=inventario)
    
    data = request.get_json() or request.form
    inventario.cantidad = data.get('cantidad', inventario.cantidad)
    inventario.cantidad_minima = data.get('cantidad_minima', inventario.cantidad_minima)
    
    db.session.commit()
    
    # Generar alerta automática
    from app.models.alerta import Alerta
    Alerta.crear_alerta(
        titulo='Inventario Modificado',
        mensaje=f'Item de inventario actualizado: {inventario.cantidad} unidades',
        tipo='inventario',
        id_usuario_destino=session.get('user_id')
    )
    
    return jsonify({'message': 'Item actualizado correctamente'})

@inventario_management_bp.route('/eliminar/<int:inventario_id>', methods=['POST'])
@login_required
@role_required('admin')
def eliminar_item_inventario(inventario_id):
    inventario = Inventario.query.get_or_404(inventario_id)
    
    db.session.delete(inventario)
    db.session.commit()
    
    # Generar alerta automática
    from app.models.alerta import Alerta
    Alerta.crear_alerta(
        titulo='Inventario Eliminado',
        mensaje=f'Item eliminado del inventario: {inventario.cantidad} unidades',
        tipo='inventario',
        id_usuario_destino=session.get('user_id')
    )
    
    return jsonify({'message': 'Item eliminado correctamente'})
