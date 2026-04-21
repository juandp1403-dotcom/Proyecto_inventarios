from functools import wraps
from flask import session, redirect, url_for, request
from app.routes.auth_helpers import get_user_role

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Rutas que no requieren login
        public_routes = ['dashboard', 'usuario.login', 'usuario.registrar']
        
        # Verificar si el usuario está logueado
        if not session.get('user_id'):
            # Si no está logueado, redirigir al dashboard
            return redirect(url_for('dashboard'))
        
        # Si está logueado pero no tiene rol, redirigir al dashboard
        current_role = get_user_role()
        if not current_role:
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def public_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function
