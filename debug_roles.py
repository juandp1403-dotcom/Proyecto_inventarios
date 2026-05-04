from app import create_app, db
from app.models.rol import Rol

app = create_app()
with app.app_context():
    # Test the exact query from the code
    rol_nombre = 'aprendiz'
    rol = Rol.query.filter_by(nombre=rol_nombre).first()
    print(f'Query for role "{rol_nombre}": {rol}')
    
    # Test with lowercase
    rol_nombre_lower = 'aprendiz'.strip().lower()
    rol_lower = Rol.query.filter_by(nombre=rol_nombre_lower).first()
    print(f'Query for lowercase role "{rol_nombre_lower}": {rol_lower}')
    
    # Show all roles
    roles = Rol.query.all()
    print('All roles in database:')
    for role in roles:
        print(f'- "{role.nombre}" (ID: {role.id})')
