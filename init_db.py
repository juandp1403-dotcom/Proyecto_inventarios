import os
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import *

def init_database(app=None):
    if app is None:
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
        
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@gmail.com')
        admin = Usuario.query.filter_by(email=admin_email).first()
        if not admin:
            admin_password = os.environ['ADMIN_PASSWORD']

            admin = Usuario(
                nombre='admin',
                email=admin_email,
                password=generate_password_hash(admin_password),
                id_rol=rol_admin.id,
                aprobado=True,
                activo=True
            )
            db.session.add(admin)
            db.session.commit()
            print(f"[+] Admin creado exitosamente: {admin_email}")
        else:
            if admin.password and not admin.password.startswith(('pbkdf2:sha256:', 'argon2:', 'scrypt:', 'bcrypt:')):
                admin.password = generate_password_hash(admin.password)
                db.session.commit()
                print("[+] Contraseña del admin guardada en texto plano fue re-hasheada.")
        
        print("Base de datos inicializada")

if __name__ == '__main__':
    init_database()