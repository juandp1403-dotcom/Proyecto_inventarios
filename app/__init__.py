from flask import Flask, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.instance_path = app.root_path

    app.config.from_object('config.Config')
    
    from datetime import timedelta
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

    db.init_app(app)

    from app.models import (
        alerta,
        ambiente,
        articulo,
        articulo_caracteristica,
        asignacion,
        caracteristica,
        categoria,
        historial_revision,
        inventario_ambiente,
        login_auditoria,
        movimiento,
        reporte,
        rol,
        solicitud,
        usuario,
    )

    from app.routes.usuario_routes import usuario_bp
    from app.routes.ambiente_routes import ambiente_bp
    from app.routes.inventario_routes import inventario_bp
    from app.routes.inventario_management import inventario_management_bp
    from app.routes.articulo_routes import articulo_bp
    from app.routes.categoria_routes import categoria_bp
    from app.routes.caracteristica_routes import caracteristica_bp
    from app.routes.articulo_caracteristica_routes import articulo_caracteristica_bp
    from app.routes.asignacion_routes import asignacion_bp
    from app.routes.movimiento_routes import movimiento_bp
    from app.routes.reporte_routes import reporte_bp
    from app.routes.solicitud_routes import solicitud_bp
    from app.routes.historial_routes import historial_bp
    from app.routes.rol_routes import rol_bp

    app.register_blueprint(usuario_bp)
    app.register_blueprint(ambiente_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(inventario_management_bp)
    app.register_blueprint(articulo_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(caracteristica_bp)
    app.register_blueprint(articulo_caracteristica_bp)
    app.register_blueprint(asignacion_bp)
    app.register_blueprint(movimiento_bp)
    app.register_blueprint(reporte_bp)
    app.register_blueprint(solicitud_bp)
    app.register_blueprint(historial_bp)
    app.register_blueprint(rol_bp)

    # Headers anti-caché para evitar problemas de templates viejos
    @app.after_request
    def add_header(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    @app.context_processor
    def inject_user():
        from app.models.usuario import Usuario
        from app.routes.auth_helpers import get_user_role

        current_role = get_user_role()
        current_user = None
        user_id = session.get('user_id')
        if user_id:
            usuario = Usuario.query.get(user_id)
            current_user = usuario.nombre if usuario else None

        return {
            'current_user': current_user,
            'current_role': current_role
        }

    @app.route('/')
    def index():
        return redirect(url_for('dashboard'))

    @app.route('/dashboard')
    def dashboard():
        from app.routes.auth_helpers import get_user_role
        return render_template('dashboard.html', current_role=get_user_role())

    return app