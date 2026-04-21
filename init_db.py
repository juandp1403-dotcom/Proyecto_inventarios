from app import create_app, db
from app.models.rol import Rol
from app.models.usuario import Usuario

def init_database():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Initialize roles if they don't exist
        roles = [
            {'nombre': 'aprendiz', 'descripcion': 'Usuario aprendiz con permisos básicos'},
            {'nombre': 'instructor', 'descripcion': 'Instructor con permisos de enseñanza'},
            {'nombre': 'auditor', 'descripcion': 'Auditor con permisos de revisión'},
            {'nombre': 'revisor', 'descripcion': 'Revisor con permisos de aprobación'},
            {'nombre': 'admin', 'descripcion': 'Administrador con permisos máximos'}
        ]
        
        for role_data in roles:
            existing_role = Rol.query.filter_by(nombre=role_data['nombre']).first()
            if not existing_role:
                new_role = Rol(nombre=role_data['nombre'], descripcion=role_data['descripcion'])
                db.session.add(new_role)
                print(f"Rol '{role_data['nombre']}' creado")
        
        # Create admin user if it doesn't exist
        admin_role = Rol.query.filter_by(nombre='admin').first()
        if admin_role:
            existing_admin = Usuario.query.filter_by(email='juanes@gmail.com').first()
            if not existing_admin:
                admin_user = Usuario(
                    nombre='Juanes',
                    email='juanes@gmail.com',
                    password='123456',
                    id_rol=admin_role.id,
                    aprobado=True,
                    activo=True
                )
                db.session.add(admin_user)
                print("Usuario admin 'Juanes' creado")
        
        # Ensure aprendiz role exists for registration
        aprendiz_role = Rol.query.filter_by(nombre='aprendiz').first()
        if not aprendiz_role:
            aprendiz_role = Rol(nombre='aprendiz', descripcion='Usuario aprendiz con permisos básicos')
            db.session.add(aprendiz_role)
            print("Rol 'aprendiz' creado")
        
        db.session.commit()
        print("Base de datos inicializada correctamente")

if __name__ == '__main__':
    init_database()
