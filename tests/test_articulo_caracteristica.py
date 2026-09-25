def test_crear_articulo_caracteristica(session):
    from app.models.articulo import Articulo
    from app.models.articulo_caracteristica import Articulo_caracteristica
    from app.models.caracteristica import Caracteristica
    from app.models.categoria import Categoria

    categoria = Categoria(nombre='Audio')
    session.add(categoria)
    session.flush()
    articulo = Articulo(
        nombre='Parlante',
        codigo='PAR-001',
        id_categoria=categoria.id,
        cantidad=3,
        estado='Disponible',
        nivel_minimo=1,
    )
    caracteristica = Caracteristica(nombre='Inalambrico')
    session.add_all([articulo, caracteristica])
    session.flush()
    relacion = Articulo_caracteristica(
        id_articulo=articulo.id,
        id_caracteristica=caracteristica.id,
    )
    session.add(relacion)
    session.commit()

    relacion_guardada = Articulo_caracteristica.query.one()
    assert relacion_guardada.id_articulo == articulo.id
    assert relacion_guardada.id_caracteristica == caracteristica.id
    assert repr(relacion_guardada) == (
        f"ArticuloCaracteristica('{articulo.id}', '{caracteristica.id}')"
    )