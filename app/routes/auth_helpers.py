from functools import wraps
from flask import jsonify, session
from app.models.usuario import Usuario
from app.models.rol import Rol


def get_user_role():
    # Primero intentar obtener el rol directamente de la sesión
    role_from_session = session.get('user_role')
    if role_from_session:
        return role_from_session
    
    # Si no está en sesión, consultarlo a la base de datos (fallback)
    user_id = session.get('user_id')
    if not user_id:
        return None

    usuario = Usuario.query.get(user_id)
    if not usuario:
        return None

    rol = Rol.query.get(usuario.id_rol)
    role_name = rol.nombre.lower() if rol else None
    
    # Guardar en sesión para futuras consultas
    session['user_role'] = role_name
    
    return role_name


def role_required(*allowed_roles):
    """Decorador para restringir acceso por rol"""
    from flask import request, redirect, url_for, jsonify
    
    allowed = [r.lower() for r in allowed_roles]
    if 'admin' not in allowed:
        allowed.append('admin')  # Admin siempre tiene acceso
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = get_user_role()
            if not role:
                # Si no hay sesión y la petición es una vista HTML, redirigir al login
                if 'application/json' not in request.headers.get('Accept', ''):
                    return redirect(url_for('dashboard'))
                return jsonify({'error': 'No autenticado'}), 401
            
            if role not in allowed:
                if 'application/json' not in request.headers.get('Accept', ''):
                    return redirect(url_for('dashboard'))
                return jsonify({'error': 'Acceso denegado', 'roles_permitidos': list(allowed_roles)}), 403
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
