from flask import Blueprint, render_template, jsonify, request, session
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
