import os
import secrets
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import *

def init_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        from app.models.rol import Rol
        from app.models.usuario import Usuario
        from app.models.categoria import Categoria
        
        for rol_name in ['admin', 'auditor', 'revisor', 'instructor', 'aprendiz']:
            if not Rol.query.filter_by(nombre=rol_name).first():
                db.session.add(Rol(nombre=rol_name))
        
        if not Categoria.query.filter_by(nombre='General').first():
            db.session.add(Categoria(nombre='General'))
        
        db.session.commit()
        
        rol_admin = Rol.query.filter_by(nombre='admin').first()
        
        if not Usuario.query.filter_by(email='admin@gmail.com').first():
            # Obtener contraseña de variable de entorno o generar una aleatoria
            admin_password = os.getenv('ADMIN_PASSWORD')
            if not admin_password:
                admin_password = secrets.token_urlsafe(12)
                print(f"[!] Variable ADMIN_PASSWORD no definida")
                print(f"[!] Contraseña generada aleatoriamente: {admin_password}")
                print(f"[!] Guarde esta contraseña y configure ADMIN_PASSWORD para futuras ejecuciones")
            
            admin = Usuario(
                nombre='admin',
                email='admin@gmail.com',
                password=generate_password_hash(admin_password),
                id_rol=rol_admin.id,
                aprobado=True,
                activo=True
            )
            db.session.add(admin)
            db.session.commit()
            print("[+] Admin creado exitosamente: admin@gmail.com")
        
        print("Base de datos inicializada")

if __name__ == '__main__':
    init_database()