from app import create_app, db
from app.models.usuario import Usuario
from app.models.rol import Rol

def create_test_users():
    app = create_app()
    with app.app_context():
        # Obtener roles
        rol_instructor = Rol.query.filter_by(nombre='instructor').first()
        rol_aprendiz = Rol.query.filter_by(nombre='aprendiz').first()
        rol_auditor = Rol.query.filter_by(nombre='auditor').first()
        rol_revisor = Rol.query.filter_by(nombre='revisor').first()
        
        # Crear usuario instructor
        instructor = Usuario.query.filter_by(email='instructor@test.com').first()
        if not instructor:
            instructor = Usuario(
                nombre='Carlos Instructor',
                email='instructor@test.com',
                password='123456',  # En producción esto debería estar hasheado
                id_rol=rol_instructor.id,
                aprobado=True,
                activo=True
            )
            db.session.add(instructor)
            print("Usuario instructor creado: instructor@test.com / 123456")
        
        # Crear usuario aprendiz
        aprendiz = Usuario.query.filter_by(email='aprendiz@test.com').first()
        if not aprendiz:
            aprendiz = Usuario(
                nombre='Ana Aprendiz',
                email='aprendiz@test.com',
                password='123456',
                id_rol=rol_aprendiz.id,
                aprobado=True,
                activo=True
            )
            db.session.add(aprendiz)
            print("Usuario aprendiz creado: aprendiz@test.com / 123456")
        
        # Crear usuario auditor
        auditor = Usuario.query.filter_by(email='auditor@test.com').first()
        if not auditor:
            auditor = Usuario(
                nombre='Luis Auditor',
                email='auditor@test.com',
                password='123456',
                id_rol=rol_auditor.id,
                aprobado=True,
                activo=True
            )
            db.session.add(auditor)
            print("Usuario auditor creado: auditor@test.com / 123456")
        
        # Crear usuario revisor
        revisor = Usuario.query.filter_by(email='revisor@test.com').first()
        if not revisor:
            revisor = Usuario(
                nombre='Maria Revisora',
                email='revisor@test.com',
                password='123456',
                id_rol=rol_revisor.id,
                aprobado=True,
                activo=True
            )
            db.session.add(revisor)
            print("Usuario revisor creado: revisor@test.com / 123456")
        
        db.session.commit()
        print("\nUsuarios de prueba creados exitosamente:")
        print("Admin: juanes@gmail.com / 123456")
        print("Instructor: instructor@test.com / 123456")
        print("Aprendiz: aprendiz@test.com / 123456")
        print("Auditor: auditor@test.com / 123456")
        print("Revisor: revisor@test.com / 123456")

if __name__ == '__main__':
    create_test_users()
