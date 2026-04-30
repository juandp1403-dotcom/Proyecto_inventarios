from app import create_app, db
from app.models.rol import Rol
import os

app = create_app()
print(f'Base de datos URI: {app.config["SQLALCHEMY_DATABASE_URI"]}')
print(f'Instancia path: {app.instance_path}')
print(f'Existe instance?: {os.path.exists(app.instance_path)}')

db_path = os.path.join(app.instance_path, 'site.db')
print(f'Path de la BD: {db_path}')
print(f'Existe BD?: {os.path.exists(db_path)}')

with app.app_context():
    print(f'\nRoles en esta app:')
    roles = Rol.query.all()
    for rol in roles:
        print(f'  {rol.nombre} (ID: {rol.id})')
    
    if len(roles) == 0:
        print('\nNo hay roles! Inicializando base de datos...')
        from init_db import init_database
        init_database()
        print('Base de datos reinicializada')
