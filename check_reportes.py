from app import create_app
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.ambiente import Ambiente

app = create_app()
with app.test_client() as client:
    # create fake revisor session if exists
    with app.app_context():
        rol_revisor = Rol.query.filter_by(nombre='revisor').first()
        revisor = Usuario.query.filter_by(id_rol=rol_revisor.id).first() if rol_revisor else None
        ambiente = Ambiente.query.first()
    if not revisor:
        print('No revisor user found')
    else:
        with client.session_transaction() as sess:
            sess['user_id'] = revisor.id
            sess['user_role'] = 'revisor'
        for path in ['/reportes/', '/reportes/nuevo', '/reportes/crear']:
            r = client.get(path)
            print(path, r.status_code)
            if r.status_code >= 400:
                print(r.get_data(as_text=True))
        # Test POST form
        if ambiente:
            r = client.post('/reportes/crear', data={'tipo': 'Inventario', 'filtros': 'prueba', 'id_ambiente': str(ambiente.id)})
            print('/reportes/crear POST', r.status_code)
            print('Location', r.headers.get('Location'))
            if r.status_code >= 400:
                print(r.get_data(as_text=True))
        else:
            print('No ambiente found')
