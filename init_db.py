import os
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
        
        admin = Usuario.query.filter_by(email='admin@gmail.com').first()
        if not admin:
            admin_password = os.getenv('ADMIN_PASSWORD', '123456')
            if 'ADMIN_PASSWORD' not in os.environ:
                print("[!] Variable ADMIN_PASSWORD no definida. Se usará la contraseña por defecto: 123456")
                print("[!] Cambie ADMIN_PASSWORD si desea un valor distinto para futuras ejecuciones.")

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
        else:
            if admin.password and not admin.password.startswith(('pbkdf2:sha256:', 'argon2:', 'scrypt:', 'bcrypt:')):
                admin.password = generate_password_hash(admin.password)
                db.session.commit()
                print("[+] Contraseña del admin guardada en texto plano fue re-hasheada.")
        
        print("Base de datos inicializada")

if __name__ == '__main__':
    init_database()