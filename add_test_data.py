from app import create_app, db
from app.models.ambiente import Ambiente
from app.models.articulo import Articulo
from app.models.inventario import Inventario
from app.models.categoria import Categoria

def add_test_data():
    app = create_app()
    with app.app_context():
        # Crear categoría general
        categoria_general = Categoria.query.filter_by(nombre='General').first()
        if not categoria_general:
            categoria_general = Categoria(
                nombre='General',
                descripcion='Categoría general para artículos'
            )
            db.session.add(categoria_general)
            db.session.commit()
            print(f"Categoría General creada con ID: {categoria_general.id}")
        
        # Crear ambiente 208
        ambiente = Ambiente.query.filter_by(nombre='Ambiente 208').first()
        if not ambiente:
            ambiente = Ambiente(
                nombre='Ambiente 208',
                tipo='Aula',
                ubicacion='Edificio Principal - Piso 2'
            )
            db.session.add(ambiente)
            db.session.commit()
            print(f"Ambiente 208 creado con ID: {ambiente.id}")
        else:
            print(f"Ambiente 208 ya existe con ID: {ambiente.id}")

        # Crear artículos para el inventario
        articulos_data = [
            {'nombre': 'Silla', 'cantidad': 10, 'codigo': 'SIL-001'},
            {'nombre': 'Computador', 'cantidad': 5, 'codigo': 'COMP-001'},
            {'nombre': 'Mesa', 'cantidad': 10, 'codigo': 'MES-001'},
            {'nombre': 'Tablero', 'cantidad': 1, 'codigo': 'TAB-001'},
            {'nombre': 'TV', 'cantidad': 1, 'codigo': 'TV-001'}
        ]

        for articulo_info in articulos_data:
            articulo = Articulo.query.filter_by(nombre=articulo_info['nombre']).first()
            if not articulo:
                articulo = Articulo(
                    nombre=articulo_info['nombre'],
                    codigo=articulo_info['codigo'],
                    descripcion=f'{articulo_info["nombre"]} para uso en ambientes',
                    id_categoria=categoria_general.id,
                    cantidad=articulo_info['cantidad'],
                    nivel_minimo=2,
                    estado='disponible'
                )
                db.session.add(articulo)
                db.session.commit()
                print(f"Artículo {articulo_info['nombre']} creado con ID: {articulo.id}")
            else:
                print(f"Artículo {articulo_info['nombre']} ya existe con ID: {articulo.id}")

            # Agregar al inventario del ambiente 208
            existencia = Inventario.query.filter_by(
                id_ambiente=ambiente.id,
                id_articulo=articulo.id
            ).first()
            
            if not existencia:
                inventario = Inventario(
                    id_ambiente=ambiente.id,
                    id_articulo=articulo.id,
                    cantidad=articulo_info['cantidad'],
                    cantidad_minima=2
                )
                db.session.add(inventario)
                print(f"Agregado {articulo_info['cantidad']} {articulo_info['nombre']} al ambiente 208")

        db.session.commit()
        print("Datos de prueba agregados exitosamente")

if __name__ == '__main__':
    add_test_data()
