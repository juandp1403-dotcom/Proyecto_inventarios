from flask import Flask, redirect, url_for, render_template, session, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.instance_path = app.root_path

    app.config.from_object('config.Config')
    
    from datetime import timedelta
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

    db.init_app(app)
    csrf.init_app(app)

    # Global Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Not found'}), 404
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden(e):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Forbidden'}), 403
        return render_template('errors/403.html'), 403

    @app.errorhandler(405)
    def method_not_allowed(e):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Method not allowed'}), 405
        return render_template('errors/403.html'), 405 # Reuse 403 or create another

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