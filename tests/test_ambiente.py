def test_crear_ambiente(session):
    from app.models.ambiente import Ambiente

    ambiente = Ambiente(
        nombre='Laboratorio 1',
        tipo='Laboratorio',
        ubicacion='Edificio A',
        descripcion='Ambiente para pruebas.',
    )
    session.add(ambiente)
    session.commit()

    ambiente_guardado = Ambiente.query.one()
    assert ambiente_guardado.nombre == 'Laboratorio 1'
    assert ambiente_guardado.ubicacion == 'Edificio A'
    assert repr(ambiente_guardado) == "Ambiente('Laboratorio 1')"


def test_ambiente_permite_campos_opcionales_vacios(session):
    from app.models.ambiente import Ambiente

    ambiente = Ambiente(nombre='Almacen', tipo='Bodega')
    session.add(ambiente)
    session.commit()

    assert ambiente.ubicacion is None
    assert ambiente.descripcion is None