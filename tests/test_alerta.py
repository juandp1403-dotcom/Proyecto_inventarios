def test_crear_alerta_para_usuario(session):
    from app.models.alerta import Alerta
    from app.models.rol import Rol
    from app.models.usuario import Usuario

    rol = Rol(nombre='admin')
    session.add(rol)
    session.flush()
    usuario = Usuario(
        nombre='usuario_alerta',
        email='alerta@example.com',
        password='secret',
        id_rol=rol.id,
    )
    session.add(usuario)
    session.flush()

    alerta = Alerta.crear_alerta(
        'Inventario bajo',
        'El articulo alcanzo el nivel minimo.',
        'inventario',
        id_usuario_destino=usuario.id,
        id_referencia=15,
    )

    assert alerta.id is not None
    assert alerta.id_usuario_destino == usuario.id
    assert alerta.id_referencia == 15
    assert alerta.leida is False
    assert repr(alerta) == "Alerta('Inventario bajo')"


def test_crear_alertas_para_roles_destino(session):
    from app.models.alerta import Alerta
    from app.models.rol import Rol
    from app.models.usuario import Usuario

    rol = Rol(nombre='auditor')
    session.add(rol)
    session.flush()
    usuario = Usuario(
        nombre='auditor_alerta',
        email='auditor@example.com',
        password='secret',
        id_rol=rol.id,
    )
    session.add(usuario)
    session.flush()

    resultado = Alerta.crear_alerta(
        'Revision pendiente',
        'Hay una revision pendiente.',
        'reporte',
    )

    assert resultado is None
    alertas = Alerta.query.filter_by(id_usuario_destino=usuario.id).all()
    assert len(alertas) == 1
    assert alertas[0].tipo == 'reporte'