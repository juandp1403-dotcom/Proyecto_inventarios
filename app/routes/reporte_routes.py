from io import BytesIO

from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app import db
from app.routes.auth_helpers import role_required, get_user_role
from app.routes.auth_decorators import login_required
from app.models.reporte import Reporte
from app.models.alerta import Alerta
from app.models.ambiente import Ambiente

reporte_bp = Blueprint('reporte', __name__, url_prefix='/reportes')


@reporte_bp.route('/', methods=['GET'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor', 'aprendiz')
def listar_reportes():
    from app.routes.auth_helpers import get_user_role
    role = get_user_role()
    if role in ['instructor', 'aprendiz']:
        reportes = Reporte.query.join(Ambiente).filter(Reporte.id_usuario == session.get('user_id')).all()
    else:
        reportes = Reporte.query.join(Ambiente).all()
    return render_template('reporte/list.html', reportes=reportes, current_role=role)


@reporte_bp.route('/pdf', methods=['GET'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor', 'aprendiz')
def descargar_reportes_pdf():
    role = get_user_role()
    if role in ['instructor', 'aprendiz']:
        reportes = Reporte.query.join(Ambiente).filter(Reporte.id_usuario == session.get('user_id')).all()
    else:
        reportes = Reporte.query.join(Ambiente).all()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50
    pdf.setTitle('Reportes de inventario')
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(50, y, 'Reportes de inventario')
    y -= 30
    pdf.setFont('Helvetica', 10)

    for reporte in reportes:
        if y < 90:
            pdf.showPage()
            pdf.setFont('Helvetica', 10)
            y = height - 50
        ambiente = reporte.ambiente.nombre if reporte.ambiente else 'N/A'
        fecha = reporte.fecha_creacion.strftime('%d/%m/%Y %H:%M:%S') if reporte.fecha_creacion else 'N/A'
        pdf.setFont('Helvetica-Bold', 11)
        pdf.drawString(50, y, f'Reporte #{reporte.id} - {reporte.tipo or "Sin tipo"}')
        y -= 17
        pdf.setFont('Helvetica', 10)
        pdf.drawString(65, y, f'Ambiente: {ambiente}')
        y -= 15
        pdf.drawString(65, y, f'Fecha: {fecha}')
        y -= 15
        pdf.drawString(65, y, f'Filtros: {reporte.filtros or "Sin filtros"}')
        y -= 25

    if not reportes:
        pdf.drawString(50, y, 'No hay reportes disponibles.')
    pdf.save()
    buffer.seek(0)
    return send_file(buffer, mimetype='application/pdf', as_attachment=True,
                     download_name='reportes_inventario.pdf')


@reporte_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor', 'aprendiz')
def crear_reporte():
    ambientes = Ambiente.query.all()
    if request.method == 'GET':
        return render_template('reporte/form.html', accion='crear', current_role=get_user_role(), ambientes=ambientes)
    
    # Manejar tanto JSON como form data
    data = request.get_json(silent=True) or request.form
    
    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400
    
    reporte = Reporte(
        tipo=data.get('tipo'),
        filtros=data.get('filtros'),
        id_usuario=session.get('user_id'),
        id_ambiente=data.get('id_ambiente')
    )
    db.session.add(reporte)
    db.session.commit()
    
    from app.models.usuario import Usuario
    from app.models.rol import Rol
    usuario = Usuario.query.get(session.get('user_id'))
    rol = Rol.query.get(usuario.id_rol) if usuario else None
    nombre_autor = usuario.nombre if usuario else 'Desconocido'
    rol_autor = rol.nombre.title() if rol else 'Desconocido'

    Alerta.crear_alerta(
        titulo='Nuevo reporte',
        mensaje=f'Se ha creado un reporte de tipo: {reporte.tipo} por {nombre_autor} ({rol_autor})',
        tipo='reporte',
        id_referencia=reporte.id
    )
    
    if request.is_json:
        return jsonify({'message': 'Reporte creado correctamente', 'id': reporte.id}), 201
    else:
        return redirect(url_for('reporte.listar_reportes'))


@reporte_bp.route('/nuevo', methods=['GET'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor', 'aprendiz')
def nuevo_reporte():
    return redirect(url_for('reporte.crear_reporte'))


@reporte_bp.route('/', methods=['POST'])
@login_required
@role_required('instructor', 'auditor', 'revisor', 'aprendiz')
def crear_reporte_api():
    data = request.get_json() or {}
    return jsonify({'message': 'Reporte generado', 'datos': data}), 201
