from functools import wraps
from flask import session, redirect, url_for
from app.models.usuario import Usuario

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            session.clear()
            return redirect(url_for('dashboard'))
        
        usuario = Usuario.query.get(user_id)
        if not usuario or not usuario.activo or not usuario.aprobado:
            session.clear()
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function
