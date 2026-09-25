def test_crear_asignacion(session):
    from app.models.ambiente import Ambiente
    from app.models.articulo import Articulo
    from app.models.asignacion import Asignacion
    from app.models.categoria import Categoria
    from app.models.rol import Rol
    from app.models.usuario import Usuario

    rol = Rol(nombre='revisor')
    categoria = Categoria(nombre='Redes')
    session.add_all([rol, categoria])
    session.flush()
    usuario = Usuario(
        nombre='revisor_asignacion',
        email='revisor@example.com',
        password='secret',
        id_rol=rol.id,
    )
    articulo = Articulo(
        nombre='Router',
        codigo='ROU-001',
        id_categoria=categoria.id,
        cantidad=5,
        estado='Disponible',
        nivel_minimo=1,
    )
    ambiente = Ambiente(nombre='Sala de redes', tipo='Sala')
    session.add_all([usuario, articulo, ambiente])
    session.flush()
    asignacion = Asignacion(
        id_usuario=usuario.id,
        id_articulo=articulo.id,
        id_ambiente=ambiente.id,
        cantidad=2,
    )
    session.add(asignacion)
    session.commit()

    asignacion_guardada = Asignacion.query.one()
    assert asignacion_guardada.id_usuario == usuario.id
    assert asignacion_guardada.id_articulo == articulo.id
    assert asignacion_guardada.id_ambiente == ambiente.id
    assert asignacion_guardada.cantidad == 2
    assert asignacion_guardada.fecha_asignacion is not None