from functools import wraps
from flask import session, redirect, url_for
from app.models.usuario import Usuario
from app.models.rol import Rol

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            session.clear()
            return redirect(url_for('dashboard'))
        
        usuario = Usuario.query.get(user_id)
        if not usuario or not usuario.activo:
            session.clear()
            return redirect(url_for('dashboard'))
        
        if not usuario.aprobado:
            rol = Rol.query.get(usuario.id_rol)
            if not rol or rol.nombre.lower() != 'aprendiz':
                session.clear()
                return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function
