def test_crear_articulo_con_categoria(session):
    from app.models.articulo import Articulo
    from app.models.categoria import Categoria

    categoria = Categoria(nombre='Computo', descripcion='Equipos tecnologicos')
    session.add(categoria)
    session.flush()
    articulo = Articulo(
        nombre='Laptop',
        codigo='LAP-001',
        descripcion='Laptop de prueba',
        id_categoria=categoria.id,
        cantidad=10,
        estado='Disponible',
        nivel_minimo=2,
        imagen='laptop.png',
    )
    session.add(articulo)
    session.commit()

    articulo_guardado = Articulo.query.one()
    assert articulo_guardado.id_categoria == categoria.id
    assert articulo_guardado.cantidad == 10
    assert articulo_guardado.fecha_publicacion is not None
    assert repr(articulo_guardado) == "Articulo('Laptop', '{}')".format(
        articulo_guardado.fecha_publicacion
    )


def test_articulo_permite_descripcion_e_imagen_vacias(session):
    from app.models.articulo import Articulo
    from app.models.categoria import Categoria

    categoria = Categoria(nombre='Mobiliario')
    session.add(categoria)
    session.flush()
    articulo = Articulo(
        nombre='Silla',
        codigo='SIL-001',
        id_categoria=categoria.id,
        cantidad=4,
        estado='Disponible',
        nivel_minimo=1,
    )

    assert articulo.descripcion is None
    assert articulo.imagen is None