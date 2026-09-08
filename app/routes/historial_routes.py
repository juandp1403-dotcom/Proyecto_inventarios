from io import BytesIO

from flask import Blueprint, render_template, jsonify, request, session, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app import db
from app.models.historial_revision import HistorialRevision
from app.models.ambiente import Ambiente
from app.routes.auth_helpers import role_required, get_user_role
from app.routes.auth_decorators import login_required

historial_bp = Blueprint('historial', __name__, url_prefix='/historial')

@historial_bp.route('/<int:ambiente_id>', methods=['GET'])
@login_required
def ver_historial(ambiente_id):
    ambiente = Ambiente.query.get_or_404(ambiente_id)
    historial = HistorialRevision.query.filter_by(id_ambiente=ambiente_id).order_by(HistorialRevision.fecha_revision.desc()).all()
    return render_template('historial/list.html', 
                         ambiente=ambiente, 
                         historial=historial,
                         current_role=get_user_role())


@historial_bp.route('/<int:ambiente_id>/pdf', methods=['GET'])
@login_required
def descargar_historial_pdf(ambiente_id):
    ambiente = Ambiente.query.get_or_404(ambiente_id)
    historial = HistorialRevision.query.filter_by(id_ambiente=ambiente_id).order_by(
        HistorialRevision.fecha_revision.desc()).all()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50
    pdf.setTitle(f'Historial de inventario - {ambiente.nombre}')
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(50, y, f'Historial de inventario: {ambiente.nombre}')
    y -= 30

    for item in historial:
        if y < 90:
            pdf.showPage()
            pdf.setFont('Helvetica', 10)
            y = height - 50
        fecha = item.fecha_revision.strftime('%d/%m/%Y %H:%M:%S') if item.fecha_revision else 'N/A'
        pdf.setFont('Helvetica-Bold', 11)
        pdf.drawString(50, y, f'{item.tipo_accion.replace("_", " ").title()} - {fecha}')
        y -= 17
        pdf.setFont('Helvetica', 10)
        pdf.drawString(65, y, f'Descripcion: {item.descripcion or "Sin descripcion"}')
        y -= 15
        if item.id_referencia:
            pdf.drawString(65, y, f'Referencia ID: {item.id_referencia}')
            y -= 15
        y -= 10

    if not historial:
        pdf.setFont('Helvetica', 10)
        pdf.drawString(50, y, 'No hay registros en el historial para este ambiente.')
    pdf.save()
    buffer.seek(0)
    return send_file(buffer, mimetype='application/pdf', as_attachment=True,
                     download_name=f'historial_inventario_{ambiente_id}.pdf')

@historial_bp.route('/api/<int:ambiente_id>', methods=['GET'])
@login_required
def api_historial(ambiente_id):
    historial = HistorialRevision.query.filter_by(id_ambiente=ambiente_id).order_by(HistorialRevision.fecha_revision.desc()).all()
    return jsonify([{
        'id': h.id,
        'fecha_revision': h.fecha_revision.isoformat(),
        'tipo_accion': h.tipo_accion,
        'descripcion': h.descripcion,
        'id_referencia': h.id_referencia
    } for h in historial])
