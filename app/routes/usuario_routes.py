from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.usuario import Usuario
from app.models.login_auditoria import Login_auditoria
from app.models.rol import Rol
from app.routes.auth_helpers import role_required, get_user_role
from app.routes.auth_decorators import login_required

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')


def record_audit_login(user_id, email, success):
    login = Login_auditoria(
        id_usuario=user_id,
        email_usuario=email,
        exitoso=success
    )
    db.session.add(login)
    db.session.commit()


@usuario_bp.route('/login', methods=['GET', 'POST'])
def login_usuario():
    if request.method == 'GET':
        return redirect(url_for('dashboard'))

    data = request.get_json(silent=True) or request.form or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email y contraseña son requeridos'}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Verificar contraseña con hash
    if not check_password_hash(usuario.password, password):
        return jsonify({'error': 'Credenciales inválidas'}), 401

    session['user_id'] = usuario.id
    # Guardar también el rol en la sesión para que persista
    rol = Rol.query.get(usuario.id_rol)
    session['user_role'] = rol.nombre.lower() if rol else None
    
    if request.form:
        return redirect(url_for('dashboard'))
    return jsonify({'message': 'Inicio de sesión exitoso', 'rol': get_user_role()})


@usuario_bp.route('/logout', methods=['GET'])
def logout_usuario():
    session.clear()
    return redirect(url_for('dashboard'))


@usuario_bp.route('/crear', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'GET':
        return render_template('usuario/crear.html', current_role=get_user_role())
    
    # POST method existing code
    data = request.get_json(silent=True) or request.form or {}
    
    # DEBUG: Ver qué datos llegan
    print(f"DEBUG - Datos recibidos: {dict(data)}")
    
    nombre = data.get('nombre', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    password_confirm = data.get('password_confirm', '').strip()
    rol_nombre = (data.get('rol') or '').strip().lower()
    
    # DEBUG: Ver valores procesados
    print(f"DEBUG - password: '{password}', password_confirm: '{password_confirm}'")

    # Validar campos requeridos con mensajes específicos
    if not nombre:
        return jsonify({'error': 'El nombre es requerido'}), 400
    if not email:
        return jsonify({'error': 'El correo electrónico es requerido'}), 400
    if not password:
        return jsonify({'error': 'La contraseña es requerida'}), 400
    if not password_confirm:
        return jsonify({'error': 'Debes confirmar la contraseña'}), 400
    if not rol_nombre:
        return jsonify({'error': 'Debes seleccionar un rol'}), 400
    
    # Validar que las contraseñas coincidan
    if password != password_confirm:
        return jsonify({'error': f'Las contraseñas no coinciden. Pass: {len(password)} chars, Confirm: {len(password_confirm)} chars'}), 400

    if rol_nombre not in ['aprendiz', 'instructor', 'auditor', 'revisor', 'admin']:
        return jsonify({'error': 'Rol inválido'}), 400

    usuario_actual = None
    current_role = get_user_role()
    if current_role:
        usuario_actual = Usuario.query.get(session.get('user_id'))

    if rol_nombre == 'admin' and current_role != 'admin':
        return jsonify({'error': 'Solo un admin puede crear usuarios admin'}), 403
    
    if rol_nombre in ['auditor', 'revisor'] and current_role not in ['auditor', 'admin']:
        return jsonify({'error': 'Solo un auditor o admin puede crear usuarios auditor o revisor'}), 403

    rol = Rol.query.filter_by(nombre=rol_nombre).first()
    if not rol:
        return jsonify({'error': 'Rol no encontrado en el sistema'}), 404

    if Usuario.query.filter_by(email=email).first():
        return jsonify({'error': 'Ya existe un usuario con ese email'}), 409
    if Usuario.query.filter_by(nombre=nombre).first():
        return jsonify({'error': 'Ya existe un usuario con ese nombre'}), 409

    aprobado = True if current_role == 'admin' or rol_nombre == 'aprendiz' else False
    nuevo_usuario = Usuario(
        nombre=nombre,
        email=email,
        password=generate_password_hash(password),
        id_rol=rol.id,
        aprobado=aprobado,
        activo=True
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    if request.form:
        return redirect(url_for('dashboard'))

    return jsonify({'message': 'Usuario creado correctamente', 'rol': rol_nombre, 'id': nuevo_usuario.id}), 201


@usuario_bp.route('/login_auditoria', methods=['POST'])
def login_auditor():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email y contraseña son requeridos'}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    success = False

    if usuario and check_password_hash(usuario.password, password):
        # Solo los auditores pueden usar esta ruta.
        rol = Rol.query.get(usuario.id_rol)
        if rol and rol.nombre.lower() == 'auditor':
            session['user_id'] = usuario.id
            success = True
        else:
            return jsonify({'error': 'Este acceso es exclusivo para auditores'}), 403
    else:
        return jsonify({'error': 'Credenciales inválidas'}), 401

    record_audit_login(usuario.id if usuario else None, email, success)
    return jsonify({'message': 'Acceso de auditor registrado', 'success': success})


@usuario_bp.route('/perfil', methods=['GET'])
@role_required('aprendiz', 'instructor', 'auditor', 'revisor')
def ver_perfil():
    user_id = session.get('user_id')
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Obtener nombre del rol
    from app.models.rol import Rol
    rol = Rol.query.get(usuario.id_rol)
    
    return render_template('usuario/perfil.html', user=usuario, rol=rol.nombre if rol else 'Desconocido')


@usuario_bp.route('/inventario', methods=['GET'])
@login_required
@role_required('instructor', 'auditor', 'revisor')
def ver_inventario():
    return jsonify({'message': 'Acceso a inventario autorizado', 'rol': get_user_role()})


@usuario_bp.route('/inventario/cambios', methods=['PUT'])
@role_required('auditor')
def cambiar_inventario():
    return jsonify({'message': 'Inventario modificado por auditor'})


@usuario_bp.route('/reportes', methods=['GET', 'POST'])
@login_required
@role_required('aprendiz', 'instructor', 'auditor', 'revisor')
def manejar_reportes():
    if request.method == 'GET':
        return jsonify({'message': 'Listado de reportes disponible'})
    return jsonify({'message': 'Reporte generado'})


@usuario_bp.route('/solicitudes', methods=['GET', 'POST'])
@login_required
@role_required('aprendiz', 'revisor')
def manejar_solicitudes():
    if request.method == 'GET':
        return jsonify({'message': 'Listado de solicitudes'})
    return jsonify({'message': 'Solicitud creada'})


@usuario_bp.route('/devoluciones', methods=['GET', 'POST'])
@login_required
@role_required('revisor')
def manejar_devoluciones():
    if request.method == 'GET':
        return jsonify({'message': 'Listado de devoluciones'})
    return jsonify({'message': 'Devolución registrada'})


@usuario_bp.route('/alertas', methods=['GET'])
@login_required
@role_required('admin', 'auditor', 'revisor', 'instructor')
def ver_alertas():
    from app.models.alerta import Alerta
    from app.models.reporte import Reporte
    from app.models.usuario import Usuario
    from app.models.rol import Rol

    user_id = session.get('user_id')
    alertas = Alerta.query.filter_by(id_usuario_destino=user_id).order_by(Alerta.fecha_creacion.desc()).all()
    alertas_dict = []

    for a in alertas:
        alerta_data = {
            'titulo': a.titulo,
            'mensaje': a.mensaje,
            'fecha': a.fecha_creacion,
            'tipo': a.tipo,
            'leida': a.leida,
            'autor': None,
            'rol_autor': None
        }

        if a.tipo == 'reporte' and a.id_referencia:
            reporte = Reporte.query.get(a.id_referencia)
            if reporte:
                autor = Usuario.query.get(reporte.id_usuario)
                if autor:
                    alerta_data['autor'] = autor.nombre
                    rol = Rol.query.get(autor.id_rol)
                    alerta_data['rol_autor'] = rol.nombre.title() if rol else None

        alertas_dict.append(alerta_data)

    return render_template('usuario/alertas.html', alerts=alertas_dict, current_role=get_user_role())


@usuario_bp.route('/listar', methods=['GET'])
@login_required
@role_required('admin')
def listar_usuarios():
    from app.routes.auth_helpers import get_user_role
    usuarios = Usuario.query.all()
    roles = Rol.query.all()
    return render_template('usuario/listar.html', usuarios=usuarios, roles=roles, current_role=get_user_role())


@usuario_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def editar_usuario(id):
    from app.routes.auth_helpers import get_user_role
    usuario = Usuario.query.get_or_404(id)
    roles = Rol.query.all()
    
    if request.method == 'POST':
        data = request.form
        usuario.nombre = data.get('nombre', usuario.nombre)
        usuario.email = data.get('email', usuario.email)
        if data.get('password'):
            usuario.password = generate_password_hash(data.get('password'))
        nuevo_rol = data.get('rol')
        if nuevo_rol:
            rol = Rol.query.filter_by(nombre=nuevo_rol).first()
            if rol:
                usuario.id_rol = rol.id
        usuario.aprobado = 'aprobado' in data
        usuario.activo = 'activo' in data
        db.session.commit()
        return redirect(url_for('usuario.listar_usuarios'))
    
    rol_actual = Rol.query.get(usuario.id_rol)
    return render_template('usuario/editar.html', usuario=usuario, roles=roles, rol_actual=rol_actual.nombre if rol_actual else None, current_role=get_user_role())


@usuario_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    
    # No permitir eliminar al admin
    if usuario.email == 'admin@gmail.com' or usuario.nombre == 'admin':
        return jsonify({'error': 'No se puede eliminar el usuario admin'}), 403
    
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado correctamente'}), 200
