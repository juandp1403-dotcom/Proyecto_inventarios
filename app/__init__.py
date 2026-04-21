from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Cargar configuración
    app.config.from_object('config.Config')

    db.init_app(app)

    # Importar modelos (IMPORTANTE)
    from app.models import (
        alerta,
        ambiente,
        articulo,
        articulo_caracteristica,
        asignacion,
        caracteristica,
        categoria,
        devolucion,
        inventario,
        login_auditoria,
        movimiento,
        reporte,
        reporte_daño,
        rol,
        solicitud,
        solicitud_detalle,
        usuario,
    )

    # Registrar rutas
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
    from app.routes.reporte_dano_routes import reporte_dano_bp
    from app.routes.solicitud_routes import solicitud_bp
    from app.routes.solicitud_detalle_routes import solicitud_detalle_bp
    from app.routes.devolucion_routes import devolucion_bp
    from app.routes.rol_routes import rol_bp
    from app.routes.login_auditoria_routes import login_auditoria_bp

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
    app.register_blueprint(reporte_dano_bp)
    app.register_blueprint(solicitud_bp)
    app.register_blueprint(solicitud_detalle_bp)
    app.register_blueprint(devolucion_bp)
    app.register_blueprint(rol_bp)
    app.register_blueprint(login_auditoria_bp)

    @app.route('/')
    def index():
        return redirect(url_for('dashboard'))

    @app.route('/dashboard')
    def dashboard():
        from app.routes.auth_helpers import get_user_role
        return render_template('dashboard.html', current_role=get_user_role())

    def init_database():
        app = create_app()
        with app.app_context():
            db.create_all()
            
            # Roles
            for rol_name in ['admin', 'auditor', 'revisor', 'instructor', 'aprendiz']:
                if not Rol.query.filter_by(nombre=rol_name).first():
                    db.session.add(Rol(nombre=rol_name))
            
            # Categoría
            if not Categoria.query.filter_by(nombre='General').first():
                db.session.add(Categoria(nombre='General'))
            
            db.session.commit()
            
            # Ambiente 208
            ambiente = Ambiente.query.filter_by(nombre='Ambiente 208').first()
            if not ambiente:
                ambiente = Ambiente(nombre='Ambiente 208', tipo='Aula', ubicacion='Edificio Principal')
                db.session.add(ambiente)
                db.session.commit()
            
            # Artículos
            articulos_data = [
                ('Silla', 'SIL-001', 10),
                ('Computador', 'COMP-001', 10),
                ('Mesa', 'MES-001', 10),
                ('Tablero', 'TAB-001', 1),
                ('TV', 'TV-001', 1)
            ]
            
            for nombre, codigo, cantidad in articulos_data:
                articulo = Articulo.query.filter_by(nombre=nombre).first()
                if not articulo:
                    db.session.add(Articulo(
                        nombre=nombre,
                        codigo=codigo,
                        descripcion=f'{nombre} para ambientes',
                        id_categoria=1,
                        cantidad=cantidad,
                        nivel_minimo=2,
                        estado='disponible'
                    ))
            
            db.session.commit()
            
            # Usuarios
            usuarios = [
                ('Admin Sistema', 'juanes@gmail.com', '123456', 'admin'),
                ('Carlos Instructor', 'instructor@test.com', '123456', 'instructor'),
                ('Ana Aprendiz', 'aprendiz@test.com', '123456', 'aprendiz'),
                ('Luis Auditor', 'auditor@test.com', '123456', 'auditor'),
                ('Maria Revisora', 'revisor@test.com', '123456', 'revisor')
            ]
            
            for nombre, email, password, rol_nombre in usuarios:
                if not Usuario.query.filter_by(email=email).first():
                    rol = Rol.query.filter_by(nombre=rol_nombre).first()
                    db.session.add(Usuario(
                        nombre=nombre,
                        email=email,
                        password=password,
                        id_rol=rol.id,
                        aprobado=True,
                        activo=True
                    ))
            
            db.session.commit()
            print("✅ Base de datos inicializada")

    return app